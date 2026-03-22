import asyncio
import websockets
import os

SERVER_URL = "ws://localhost:8000/chat"
PROFILE_FILE = "user_profile.txt" # The file where we save the username

def get_or_create_user():
    """Checks if the computer already remembers a username."""
    if os.path.exists(PROFILE_FILE):
        # Read the saved name
        with open(PROFILE_FILE, "r") as file:
            saved_name = file.read().strip()
            print(f"👋 Welcome back, {saved_name}!")
            return saved_name
    else:
        # First time running the app on this computer
        print("=== Account Setup ===")
        new_name = input("Enter a new username to register: ").strip()
        
        # Save it to the file for next time
        with open(PROFILE_FILE, "w") as file:
            file.write(new_name)
            
        print(f"✅ Saved! This computer will now remember you as '{new_name}'.")
        return new_name

async def listen_to_server(websocket):
    """Listens for messages and prints them cleanly without messy arrows."""
    try:
        while True:
            message = await websocket.recv()
            print(f"{message}") # Just a clean, standard print
    except:
        pass 

async def chat():
    # 1. Get the user from memory (or ask if they are new)
    username = get_or_create_user()

    try:
        async with websockets.connect(SERVER_URL) as server:
            print("\n✅ Connected to chat. You can start typing below!")
            print("-" * 40) # A clean dividing line

            # 2. Turn on the background listener
            listener_task = asyncio.create_task(listen_to_server(server))

            # 3. Let the user type (Cleanly, with no weird arrows)
            while True:
                message = await asyncio.to_thread(input, f"{username}> ")
                
                if message.lower() == "/exit":
                    print("Exiting chat. Goodbye!")
                    listener_task.cancel()
                    break

                if message:
                    await server.send(f"{username}: {message}")

    except ConnectionRefusedError:
        print("❌ Could not connect to the server. Is uvicorn running?")

if __name__ == "__main__":
    asyncio.run(chat())