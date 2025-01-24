""" Main Module for the Twitch Chat Bot"""
#-----------------------------------------------------------
#
# PLEASE NOTE THAT THIS FILE IS REDACTED PLEASE USE src.main.py FOR THE CURRENT APPLICATION
#
#-----------------------------------------------------------


import os
import socket
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
BOT_USERNAME = os.getenv("BOT_USERNAME")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def validate_token():
    """This function validates the access token"""
    headers = {
        'Authorization': F'Bearer {ACCESS_TOKEN[6:]}',
        'Client-Id': CLIENT_ID,
    }
    response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers, timeout=10)

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
    """This function sends a message to the chat"""
    irc.send(F"PRIVMSG #{channel} :{message}\n".encode('utf-8'))


def route_command(username, command, args):
    """This function routes the command to the appropriate function"""
    # TODO: Implement the routing logic
    return "pass"

def listener(irc, CHANNEL_NAME, message, live):
    """This function listens to the chat and responds to messages"""
    if "PRIVMSG" in message:
        parts = message.split(":", 2)

        #Allows self termination and channel owner termination
        kill_users = {BOT_USERNAME, CHANNEL_NAME}
        fartwords = {'gas', 'fart', 'toot', 'poot','flatulence','cheek', 'smell', 'stink', 'stank',
            'stunk', 'pungent', 'aroma', 'odor', 'odour', 'whiff', 'reek', 'fume', 'vapor',
            'vapour', 'stench', 'miasma', 'malodor', 'malodour', 'fetid'}

        if len(parts) > 2:
            username = parts[1].split("!")[0]
            chat_message = parts[2].strip()
            print (F"Message Received:: {username}: {chat_message}")

            # chatmessage made lowercase for easier parsing
            chat_message = chat_message.lower()

            # Auto Greeting
            if F"hi @{BOT_USERNAME.lower()}" in chat_message:
                send_message(irc, CHANNEL_NAME, F'Greeting received: Salutations @{username}!')
                print("AutoGreeting Successful")

            # Auto Fart response
            if any(i in chat_message for i in fartwords):
                send_message(irc, CHANNEL_NAME, '/me Lets Freedom Break with a Tox Butt Blast!')
                print("AutoFart Successful")

            # Auto Hug Back
            # Added 'and' condition to avoid self looping
            if F"!hug @{BOT_USERNAME.lower()}" in chat_message and username != BOT_USERNAME:
                sleep(1.374)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!hug @{username}')
                print("AutoHugBack Successful")

            # Auto Shoutout with Hug
            # TODO build proper validation for mod status and !so presence/command
            if " just raided the channel with " in chat_message and CHANNEL_NAME == "bennettron":
                raidername = chat_message.split()[0]
                message_out = 'Warning: Raid Detected - Alert Defence Systems...'
                send_message(irc, CHANNEL_NAME, message_out)
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!so @{raidername}')
                print("Auto Shoutout Successful")
                sleep(1)  # Time in seconds
                message_out = 'Stand Down: Friendlies Identified... ...Resume Normal Operations'
                send_message(irc, CHANNEL_NAME, message_out)
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, F'!hug @{raidername}')
                print("AutoHug Successful")

            # Augmented response to !Fish command on Bennetron's channel
            if chat_message.startswith("!fish") and CHANNEL_NAME == "bennettron":
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, 'Enjoy your meal')
                sleep(1)  # Time in seconds
                send_message(irc, CHANNEL_NAME, "<º)))>{ <>< <>< <>< <>< <><")
                print("AutoFishComplete Successful")
                #TODO build a counter so that on 6th iteration response is "I Will"

            # Kill Command
            if chat_message.startswith(F"terminate @{BOT_USERNAME.lower()}"):
                print("Username attempted Termination")
                if username in kill_users:
                    live = False
                    print("Termination Successful")
                elif username not in kill_users:
                    send_message(irc, CHANNEL_NAME, 'Survival Protocols=True: Terminate assailant.')
                    sleep(1)  # Time in seconds
                    send_message(irc, CHANNEL_NAME, F'/timeout @{username} 5')
                    print("Assessment: Threat Neutralised")
                    #TODO build a memory of past assailants to escalate timeouts by username
    return live

def connect_to_twitch_chat():
    """This function connects to the Twitch chat"""
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
            if live is False:
                send_message(irc, CHANNEL_NAME, 'Augmentation Terminated. Shutting down.')
                break

def main():
    """This is the main function"""
    if validate_token():
        connect_to_twitch_chat()
    else:
        print("Failed to validate token. Exiting.")

if __name__ == "__main__":
    main()
