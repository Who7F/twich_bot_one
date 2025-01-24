"""This module is responsible for managing the chat connection and handling the messages."""
from bot.utility_functions import send_message
from bot.listener import listener


def handle_ping(irc, massage):
    """Handle the ping message from the server."""
    if massage.startswith("PING"):
        irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))


def manage_chat_connection(irc, bot_username, channel_name, commands):
    """Manage the chat connection and handle the messages."""
    print(f"Connected to {channel_name}'s as {bot_username}")

    start_bot = f"{bot_username} is now a bot!"
    end_bot = "Time for Tubbie Bye Bye"
    send_message(irc, channel_name, start_bot)

    while True:
        message = irc.recv(2048).decode('utf-8')
        handle_ping(irc, message)

        if "PRIVMSG" in message:
            stay_alive = listener(irc, channel_name, bot_username, message, commands)

            if not stay_alive:
                send_message(irc, channel_name, end_bot)
                break
