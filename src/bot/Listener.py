"""This module contains the listener function that listens and responds to the chat commands."""
import asyncio
from .utility_functions import send_message

async def delayed_response(irc, channel_name, response, delay):
    await ssyncio.sleep(delay)
    send_message(irc, channel_name, response)


def make_response(irc, username, channel_name, bot_username, command, commands):
    """This function makes a response to the chat commands."""
    for cmd, data in commands["chatCommands"].items():
        if command == cmd or command in data.get("aliases", []):
            response = data["response"].replace("{BOT_USERNAME}", bot_username)
            response = data["response"].replace("{username}", username)

            if data["sleeptime"]:
                asyncio.create_task(delayed_response(irc, channel_name, response, data["sleeptime"]))
            else:
                send_message(irc, channel_name, response)


def listener(irc, channel_name, bot_username, message, commands):
    """This function listens to the chat and responds to the chat commands."""
    if "PRIVMSG" in message:
        parts = message.split(":", 2)
        kill_users = {bot_username}# todo. Plug this in with commands
        
        if len(parts) > 2:
            username = parts[1].split("!")[0]
            chat_message = parts[2].strip()

            if chat_message.startswith(f"@{bot_username} KILL"):
                if username in kill_users:
                    return False

            chat_message = chat_message.lower()

            if chat_message.startswith(f"hello @{bot_username}"):
                send_message(irc, channel_name, f'@{username} I am not a bot')

            if chat_message.startswith("!"):
                split_message  = chat_message.split(" ")
                command = split_message[0]
                make_response(irc, username, channel_name, bot_username, command, commands)

    return True
