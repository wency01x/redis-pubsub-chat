import os
import redis
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# The Server unlocks the Upstash Database
db = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True
)

connected_clients = []
HISTORY_KEY = "chat:general:history" # The name of our digital filing cabinet

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    # --- 1. THE CATCH-UP PHASE (Backreading) ---
    # Grab the last 50 messages from the Redis List (-50 to -1)
    recent_messages = db.lrange(HISTORY_KEY, -50, -1)
    for msg in recent_messages:
        # Send the history to the new person who just joined
        await websocket.send_text(msg)
    # -------------------------------------------

    try:
        while True:
            # Waiter receives the new message
            data = await websocket.receive_text()
            print(f"Server received: {data}")
            
            # --- 2. THE SAVING PHASE (Persistence) ---
            # Push the new message to the very end of the Redis List
            db.rpush(HISTORY_KEY, data)
            
            #Trim the list to only keep the newest 50. 
            # This stops Free Tier database from getting completely full
            db.ltrim(HISTORY_KEY, -50, -1)
            # -----------------------------------------

            # Waiter broadcasts it to everyone currently online
            for client in connected_clients:
                await client.send_text(data)
                
    except:
        # Remove user if they quit or disconnect
        if websocket in connected_clients:
            connected_clients.remove(websocket)