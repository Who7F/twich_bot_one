import os
from dotenv import load_dotenv
from bot import validateToken, connectTwitchChat, listener

def send_message(irc, channel, message):
    irc.send(f"PRIVMSG #{channel} :{message}\n".encode('utf-8'))


def route_command(username, command, args):
    return "pass"

def connect(irc, BOT_USERNAME, CHANNEL_NAME):
    
    print(f"Connected to {CHANNEL_NAME}'s chat as {BOT_USERNAME}")
    
    bot_message = "maize_13 is now a bot!"
    send_message(irc, CHANNEL_NAME, bot_message)

    while True:
        message = irc.recv(2048).decode('utf-8')
        if message.startswith("PING"):
            irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
        else:
            live = listener(irc, CHANNEL_NAME, BOT_USERNAME, message)

            if live == False:
                send_message(irc, CHANNEL_NAME, f'Time for Tubbie Bye Bye')
                break

def main():
    load_dotenv()

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  
    CLIENT_ID = os.getenv("CLIENT_ID")        
    BOT_USERNAME = os.getenv("BOT_USERNAME")  
    CHANNEL_NAME = os.getenv("CHANNEL_NAME")  

    # Todo. Remove when everyone as updated there Access token
    if ACCESS_TOKEN.startswith("oauth:"):
        ACCESS_TOKEN = ACCESS_TOKEN[6:]
        print(f"remove oauth: form ACCESS_TOKEN")
        
    if validateToken(ACCESS_TOKEN, CLIENT_ID):
        irc = connectTwitchChat(ACCESS_TOKEN, BOT_USERNAME, CHANNEL_NAME)
        connect(irc, BOT_USERNAME, CHANNEL_NAME)
    else:
        print("Failed to validate token. Exiting.")

if __name__ == "__main__":
    main()
