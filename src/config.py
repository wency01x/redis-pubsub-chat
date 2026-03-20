import os 
import redis 
from dotenv import load_dotenv

#load secret variabes from env file
load_dotenv()

def get_redis_connection():
    try:
        host = os.getenv("REDIS_HOST", "localhost")
        port = os.getenv("REDIS_PORT", 6379)
        password = os.getenv("REDIS_PASSWORD", None)

        client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
            ssl=True
        )

        if client.ping():
            return client
    
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

if __name__ == "__main__":
    #a quick test to run later
    if get_redis_connection():
        print("Successfully connected to Redis!")