"""This is the main file that will be run when the script is executed."""
import os
import json
from dotenv import load_dotenv
from bot import connect_twitch_chat, manage_chat_connection


# TODO. Move to utility_functions.py. Path will change to ../../config/filename
def load_commands(filepath):
    """Load the commands from the file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """This is the main function that will be called when the script is run."""
    load_dotenv()
    file_name = "../config/commands.json"
    commands = load_commands(file_name)

    access_token = os.getenv("ACCESS_TOKEN")
    client_id = os.getenv("CLIENT_ID")
    bot_username = os.getenv("BOT_USERNAME")
    channel_name = os.getenv("CHANNEL_NAME")

    irc = connect_twitch_chat(access_token, client_id, bot_username, channel_name)
    if irc:
        manage_chat_connection(irc, bot_username, channel_name, commands)

    else:
        # TODO. Add Exception handling
        print("Failed Relay Chat. Exiting.")
    print("END")


if __name__ == "__main__":
    main()
