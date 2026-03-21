import sys
import threading
import time
from config import get_redis_connection
from display_worker import listen_for_messages

def main():
    print("Welcome to Redis-PubSub-Chat")
    
    client = get_redis_connection()
    if not client:
        print("Could not connect to Redis. Please check your .env file or server status.")
        sys.exit(1)

    username = input("Enter your username: ").strip()
    channel = input("Enter channel to join (e.g., general): ").strip()
    
    # password check
    lockbox_key = "channel_passwords"
    expected_password = client.hget(lockbox_key, "general")

    if expected_password:
        attempt = input (f"'{channel}'is locked. Enter password: ")
        if attempt != expected_password:
            print("Incorrect password. Access Denied.")
            sys.exit(1)
        print("Password accepted. Joining channel...")

    if not username or not channel:
        print("Username and channel are required.")
        sys.exit(1)

    # add user to the redis set for the channel
    users_key = f"channel:{channel}:users"
    client.sadd(users_key, username)

    # announce arrival to everyone else
    client.publish(channel, f"[SERVER] {username} has joined the chat!")

    # Start the background listener thread to receive messages
    listener_thread = threading.Thread(
        target=listen_for_messages, 
        args=(client, channel, username),
        daemon=True 
    )
    listener_thread.start()

    # Give the thread a tiny fraction of a second to print its "Joined" message
    time.sleep(0.1)

    print("\n[Commands: /online, /quit, /lock <pass>, /unlock]")
    
    # The Publisher Loop: This keeps the terminal open forever so you can type
    try:
        while True:
            message = input(f"{username} > ")
                
            if message.lower() == '/quit':
                print("Exiting chat...")
                break
                
            elif message.lower() == '/online':
                    # smembers grabs all the names we format into a clear string
                online_users = client.smembers(users_key)
                users_list = ", ".join(online_users) 
                print(f"\n[SERVER] Users currently in {channel}: {users_list}\n")

            elif message.lower().startswith('/lock '):
                # splits "/lock my password" into two parts
                parts = message.split(' ', 1)
                new_password = parts[1]
                client.hset(lockbox_key, channel, new_password)
                print(f"\n[SERVER] You locked '{channel}' users will need a password.\n")
            
            elif message.lower() == '/unlock':
                client.hdel(lockbox_key, channel)
                print(f"\n[SERVER] You unlocked '{channel}'. Anyone can join now.\n")

            elif message:
                formatted_message = f"{username}: {message}"
                client.publish(channel, formatted_message)
                    
    except KeyboardInterrupt:
        print("\nExiting chat...")

    finally:
    # clean up: remove user from the channel set and announce departure
        client.srem(users_key, username)
        client.publish(channel, f"[SERVER] {username} has left the chat.")

if __name__ == "__main__":
    main()