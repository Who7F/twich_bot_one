import socket
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  
CLIENT_ID = os.getenv("CLIENT_ID")        
BOT_USERNAME = os.getenv("BOT_USERNAME")  
CHANNEL_NAME = os.getenv("CHANNEL_NAME")  

# Validate the Access Token
def validate_token():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN[6:]}',
        'Client-Id': CLIENT_ID,
    }
    response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)

    if response.status_code == 200:
        print("Token is valid.")
        data = response.json()
        print(f"Bot Username: {data['login']}")
        print(f"Scopes: {data['scopes']}")
        return True
    else:
        print("Token validation failed.")
        print(response.json())
        print(ACCESS_TOKEN)
        return False

def send_message(irc, channel, message):
    irc.send(f"PRIVMSG #{channel} :{message}\n".encode('utf-8'))


def route_command(username, command, args):
    return "pass"

def listener(irc, CHANNEL_NAME, message, live):
    if "PRIVMSG" in message:
        parts = message.split(":", 2)
        kill_users = {"intoxic_hate", BOT_USERNAME}
        if len(parts) > 2:
            username = parts[1].split("!")[0]
            chat_message = parts[2].strip()
            if chat_message.startswith(f"@{BOT_USERNAME} KILL"):
                print(username)
                if username in kill_users:
                    live = False
            chat_message = chat_message.lower()
            
            if chat_message.startswith(f"hello @{BOT_USERNAME}"):
                send_message(irc, CHANNEL_NAME, f'@{username} I am not a bot')
            
            if chat_message.startswith("!"):
                print("!")
                split_message  = chat_message.split(" ")
                command = split_message[0]
                args = split_message[1:]
                response = route_command(username, command, args)
                send_message(irc, CHANNEL_NAME, f'@{username} hello hotstuff')
    return(live)
        

def connect_to_twitch_chat():
    SERVER = "irc.chat.twitch.tv"
    PORT = 6667

    irc = socket.socket()
    irc.connect((SERVER, PORT))
    irc.send(f"PASS {ACCESS_TOKEN}\n".encode('utf-8')) #to be changed
    irc.send(f"NICK {BOT_USERNAME}\n".encode('utf-8'))
    irc.send(f"JOIN #{CHANNEL_NAME}\n".encode('utf-8'))

    print(f"Connected to {CHANNEL_NAME}'s chat as {BOT_USERNAME}")
    live = True

    bot_message = "maize_13 is now a bot!"
    send_message(irc, CHANNEL_NAME, bot_message)

    while True:
        message = irc.recv(2048).decode('utf-8')
        if message.startswith("PING"):
            irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
        else:
            live = listener(irc, CHANNEL_NAME, message, live)
            print(live)
            if live == False:
                send_message(irc, CHANNEL_NAME, f'Time for Tubbie Bye Bye')
                break

def main():
    if validate_token():
        connect_to_twitch_chat()
    else:
        print("Failed to validate token. Exiting.")

if __name__ == "__main__":
    main()
