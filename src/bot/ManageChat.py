from bot.Listener import listener
from .Utils import sendMessage

def headlePing(irc, massage):
    if massage.startswith("PING"):
        irc.send("PONG :tmi.twitch.tv\n".encode('utf-8'))


def manageChatConnection(irc, BOT_USERNAME, CHANNEL_NAME, commands):
    print(f"Connected to {CHANNEL_NAME}'s as {BOT_USERNAME}")

    start_bot = f"{BOT_USERNAME} is now a bot!"
    end_bot = f"Time for Tubbie Bye Bye"
    sendMessage(irc, CHANNEL_NAME, start_bot)

    while True:
        message = irc.recv(2048).decode('utf-8')
        headlePing(irc, message)

        if "PRIVMSG" in message:
            isLive = listener(irc, BOT_USERNAME, CHANNEL_NAME, message, commands)

            if not isLive:
                sendMessage(irc, CHANNEL_NAME, end_bot)
                break
