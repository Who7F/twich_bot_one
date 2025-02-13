"""This module is responsible for managing the chat connection and handling the messages."""
from .utility_functions import send_message
from .listener import listener
import asyncio


def handle_ping(irc, massage):
    """Handle the ping message from the server."""
    if massage.startswith("PING"):
        irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))


async def manage_chat_connection(irc, bot_username, channel_name, commands):
    """Manage the chat connection and handle the messages."""
    print(f"Connected to {channel_name}'s as {bot_username}")

    start_bot = commands["botCommands"]["start_bot"].format(bot_username=bot_username)
    stop_bot = commands["botCommands"]["stop_bot"].format(bot_username=bot_username)

    send_message(irc, channel_name, start_bot)

    while True:
        await asyncio.sleep(0.1)
        print('loop')
        message = irc.recv(2048).decode('utf-8')
        handle_ping(irc, message)
        

        if "PRIVMSG" in message:
            stay_alive = await listener(irc, channel_name, bot_username, message, commands)

            if not stay_alive:
                send_message(irc, channel_name, stop_bot)
                break
