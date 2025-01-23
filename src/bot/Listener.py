def listener(irc, CHANNEL_NAME, BOT_USERNAME, message):
    if "PRIVMSG" in message:
        parts = message.split(":", 2)
        kill_users = {BOT_USERNAME}
        if len(parts) > 2:
            username = parts[1].split("!")[0]
            chat_message = parts[2].strip()
            
            if chat_message.startswith(f"@{BOT_USERNAME} KILL"):
                if username in kill_users:
                    return False
                
            chat_message = chat_message.lower()
            
            if chat_message.startswith(f"hello @{BOT_USERNAME}"):
                send_message(irc, CHANNEL_NAME, f'@{username} I am not a bot')
            
            if chat_message.startswith("!"):
                print("!")
                split_message  = chat_message.split(" ")
                command = split_message[0]
                args = split_message[1:]
                #todo. This is where routs is going to be called
                response = route_command(username, command, args)
                send_message(irc, CHANNEL_NAME, f'@{username} hello hotstuff')
    return True
