import socket
import requests
def validateToken(ACCESS_TOKEN, CLIENT_ID):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Client-Id': CLIENT_ID,
    }
    response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)

    if response.status_code == 200:
        print("Token is valid.")
        data = response.json()
        print(f"Bot Username: {data['login']}")
        print(f"Scopes: {data['scopes']}")
        return True
    else:
        print("Token validation failed.")
        print(response.json())
        return False


def connectTwitchChat(ACCESS_TOKEN, CLIENT_ID, BOT_USERNAME, CHANNEL_NAME):
    if validateToken(ACCESS_TOKEN, CLIENT_ID):
        SERVER = "irc.chat.twitch.tv"
        PORT = 6667

        irc = socket.socket()
        irc.connect((SERVER, PORT))
        irc.send(f"PASS oauth:{ACCESS_TOKEN}\n".encode('utf-8')) 
        irc.send(f"NICK {BOT_USERNAME}\n".encode('utf-8'))
        irc.send(f"JOIN #{CHANNEL_NAME}\n".encode('utf-8'))

        print(f"Connected to {CHANNEL_NAME}'s chat as {BOT_USERNAME}")
        return irc
    print("Failed to validate token. Exiting.")
