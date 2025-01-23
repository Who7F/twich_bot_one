import socket

def connectTwitchChat(ACCESS_TOKEN, BOT_USERNAME, CHANNEL_NAME):
    SERVER = "irc.chat.twitch.tv"
    PORT = 6667

    irc = socket.socket()
    irc.connect((SERVER, PORT))
    irc.send(f"PASS oauth:{ACCESS_TOKEN}\n".encode('utf-8')) 
    irc.send(f"NICK {BOT_USERNAME}\n".encode('utf-8'))
    irc.send(f"JOIN #{CHANNEL_NAME}\n".encode('utf-8'))

    print(f"Connected to {CHANNEL_NAME}'s chat as {BOT_USERNAME}")
    return irc
