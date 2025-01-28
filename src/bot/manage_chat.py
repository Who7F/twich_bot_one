from .listener import listener
from .utils import send_message

def headle_ping(irc, massage):
    if massage.startswith("PING"):
        irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))


def manage_chat_connection(irc, bot_username, channel_name, commands):
    print(f"Connected to {channel_name}'s as {bot_username}")

    start_bot = commands["botCommands"]["start_bot"].format(bot_username=bot_username)
    stop_bot = commands["botCommands"]["stop_bot"].format(bot_username=bot_username)
    send_message(irc, channel_name, start_bot)

    while True:
        message = irc.recv(2048).decode('utf-8')
        headle_ping(irc, message)

        if "PRIVMSG" in message:
            keep_live = listener(irc, bot_username, channel_name, message, commands)

            if not keep_live:
                send_message(irc, channel_name, stop_bot)
                break
