def listen_for_messages(redis_client, channel_name, username):
    """
    Runs in a background thread, constantly listening for new messages.
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel_name)
    
    print(f"\n[*] Joined channel: '{channel_name}'. Waiting for messages...\n")

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            
            # Don't print the message if you are the one who sent it
            if not data.startswith(f"{username}:"):
                # \r clears the current line so incoming text doesn't mess up your typing
                print(f"\r{data}")
                # Reprint your prompt so you know you can still type
                print(f"{username} > ", end="", flush=True)