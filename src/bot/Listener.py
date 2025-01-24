from .Utils import sendMessage

def makeResponse(irc, username, CHANNEL_NAME, BOT_USERNAME, command, args, commands):
    for cmd, data in commands["chatCommands"].items():
        if command == cmd or command in data.get("aliases", []):
            response = data["response"].replace("{BOT_USERNAME}", BOT_USERNAME).replace("{username}", username)
            sendMessage(irc, CHANNEL_NAME, response)


def listener(irc, CHANNEL_NAME, BOT_USERNAME, message, commands):
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
                sendMessage(irc, CHANNEL_NAME, f'@{username} I am not a bot')
            
            if chat_message.startswith("!"):
                split_message  = chat_message.split(" ")
                command = split_message[0]
                args = split_message[1:]
                makeResponse(irc, username, CHANNEL_NAME, BOT_USERNAME, command, args, commands)
    return True
