import socket
import os
import requests
from dotenv import load_dotenv
from time import sleep

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  
CLIENT_ID = os.getenv("CLIENT_ID")        
BOT_USERNAME = os.getenv("BOT_USERNAME")  
CHANNEL_NAME = os.getenv("CHANNEL_NAME")  

# Validate the Access Token
def validate_token():
    headers = {
        'Authorization': F'Bearer {ACCESS_TOKEN[6:]}',
        'Client-Id': CLIENT_ID,
    }
    response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)

    if response.status_code == 200:
        print("Token is valid.")
        data = response.json()
        print(F"Bot Username: {data['login']}")
        print(F"Scopes: {data['scopes']}")
        return True
    else:
        print("Token validation failed.")
        print(response.json())
        return False

def send_message(irc, channel, message):
    irc.send(F"PRIVMSG #{channel} :{message}\n".encode('utf-8'))


def route_command(username, command, args):
    return "pass"

def listener(irc, CHANNEL_NAME, message, live):
    if "PRIVMSG" in message:
        parts = message.split(":", 2)
        
        #Allows self termination and channel owner termination
        kill_users = {BOT_USERNAME, CHANNEL_NAME}
        fartwords = {'gas', 'fart', 'toot', 'poot','flatulence','cheek', 'smell', 'stink', 'stank', 'stunk', 'pungent', 'aroma', 'odor', 'odour', 'whiff', 'reek', 'fume', 'vapor', 'vapour', 'stench', 'reek', 'miasma', 'malodor', 'malodour', 'fetid'}
        
        if len(parts) > 2:
            username = parts[1].split("!")[0]
            chat_message = parts[2].strip()
            print (F"Message Received:: {username}: {chat_message}")
        
            # chatmessage made lowercase for easier parsing
            chat_message = chat_message.lower()

            # Auto Greeting
            if chat_message.__contains__(F"hi @{BOT_USERNAME.lower()}"):
                send_message(irc, CHANNEL_NAME, F'Greeting received: Salutations @{username}!')
                print(F"AutoGreeting Successful")

            # Auto Fart response
            if any(i in chat_message for i in fartwords):
                send_message(irc, CHANNEL_NAME, F'/me Lets Freedom Break with a Tox Butt Blast!')
                print(F"AutoFart Successful")

            # Auto Hug Back
            # Added 'and' condition to avoid self looping
            if chat_message.__contains__(F"!hug @{BOT_USERNAME.lower()}") and username != BOT_USERNAME:
                sleep(1.374)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!hug @{username}')
                print(F"AutoHugBack Successful")
                        
            # Auto Shoutout with Hug
            # TODO build proper validation for mod status and !so presence/command
            if chat_message.__contains__(" just raided the channel with ") and CHANNEL_NAME == "bennettron":
                # todo: extract raidername from chat_message
                raidername = chat_message.split()[0]
                send_message(irc, CHANNEL_NAME, F'Warning: Raid Detected - Alert Defence Systems...')
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!so @{raidername}')
                print(F"Auto Shoutout Successful")
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'Stand Down: Friendlies Identified...   ...Resume Normal Operations')
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!hug @{raidername}')
                print(F"AutoHug Successful")
            
            # Augmented response to !Fish command on Bennetron's channel
            if chat_message.startswith("!fish") and CHANNEL_NAME == "bennettron":
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, 'Enjoy your meal')
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, "<º)))>{ <>< <>< <>< <>< <><")
                print(F"AutoFishComplete Successful")
                #TODO build a counter so that on 6th iteration - response = "I Will" instead of the fish

            # Kill Command
            if chat_message.startswith(F"terminate @{BOT_USERNAME.lower()}"):
                print(F"Username attempted Termination")
                if username in kill_users:
                    live = False
                    print(F"Termination Successful")
                elif username not in kill_users:
                    send_message(irc, CHANNEL_NAME, F'Survival Protocols initiated: Terminate assailant...')
                    sleep(1)  # Time in seconds
                    send_message(irc, CHANNEL_NAME, F'/timeout @{username} 5')
                    print(F"Assessment: Threat Neutralised")
                    #TODO build a memory of past assailants to escalate timeouts by username
    return(live)        

def connect_to_twitch_chat():
    SERVER = "irc.chat.twitch.tv"
    PORT = 6667

    irc = socket.socket()
    irc.connect((SERVER, PORT))
    irc.send(F"PASS {ACCESS_TOKEN}\n".encode('utf-8')) #to be changed
    irc.send(F"NICK {BOT_USERNAME}\n".encode('utf-8'))
    irc.send(F"JOIN #{CHANNEL_NAME}\n".encode('utf-8'))

    print(F"Connected to {CHANNEL_NAME}'s chat as {BOT_USERNAME}")
    live = True

    bot_message = F"{BOT_USERNAME} is now augmented!"
    send_message(irc, CHANNEL_NAME, bot_message)

    while True:
        message = irc.recv(2048).decode('utf-8')
        if message.startswith("PING"):
            irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
        else:
            live = listener(irc, CHANNEL_NAME, message, live)
            if live == False:
                send_message(irc, CHANNEL_NAME, F'Augmentation Terminated. Shutting down.')
                break

def main():
    if validate_token():
        connect_to_twitch_chat()
    else:
        print("Failed to validate token. Exiting.")

if __name__ == "__main__":
    main()
