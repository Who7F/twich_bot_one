import os
import json
from dotenv import load_dotenv
from bot import connect_twitch_chat, manage_chat_connection


# Todo. Move to Utils.py. Path will change to ../../config/filename
def loadCommands(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def main():
    load_dotenv()
    file_name = "../config/commands.json"
    commands = loadCommands(file_name)
        
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  
    CLIENT_ID = os.getenv("CLIENT_ID")        
    BOT_USERNAME = os.getenv("BOT_USERNAME")  
    CHANNEL_NAME = os.getenv("CHANNEL_NAME")  

    # Todo. Remove when everyone as updated there Access token
    if ACCESS_TOKEN.startswith("oauth:"):
        ACCESS_TOKEN = ACCESS_TOKEN[6:]
        print(f"remove oauth: form ACCESS_TOKEN")
        
    
    irc = connect_twitch_chat(ACCESS_TOKEN, CLIENT_ID, BOT_USERNAME, CHANNEL_NAME)
    if irc:
        manage_chat_connection(irc, BOT_USERNAME, CHANNEL_NAME, commands)
    else:
        print("Failed Relay Chat. Exiting.")
    print("END")
    

if __name__ == "__main__":
    main()
