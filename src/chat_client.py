import sys
import threading
import time
from config import get_redis_connection
from display_worker import listen_for_messages

def main():
    print("=== Welcome to Redis-PubSub-Chat ===")
    
    client = get_redis_connection()
    if not client:
        print("Could not connect to Redis. Please check your .env file or server status.")
        sys.exit(1)

    username = input("Enter your username: ").strip()
    channel = input("Enter channel to join (e.g., general): ").strip()
    
    if not username or not channel:
        print("Username and channel are required.")
        sys.exit(1)

    # Start the background listener thread to receive messages
    listener_thread = threading.Thread(
        target=listen_for_messages, 
        args=(client, channel, username),
        daemon=True 
    )
    listener_thread.start()

    # Give the thread a tiny fraction of a second to print its "Joined" message
    time.sleep(0.1)

    print("[Type your message and press Enter. Type '/quit' to exit.]")
    
    # The Publisher Loop: This keeps the terminal open forever so you can type!
    while True:
        try:
            message = input(f"{username} > ")
            
            if message.lower() == '/quit':
                print("Exiting chat...")
                break
                
            if message:
                formatted_message = f"{username}: {message}"
                client.publish(channel, formatted_message)
                
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

if __name__ == "__main__":
    main()