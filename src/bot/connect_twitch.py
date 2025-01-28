import socket
import requests
def validate_token(access_token, client_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
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


def connect_twitch_chat(access_token, client_id, bot_username, channel_name):
    if validate_token(access_token, client_id):
        SERVER = "irc.chat.twitch.tv"
        PORT = 6667

        irc = socket.socket()
        irc.connect((SERVER, PORT))
        irc.send(f"PASS oauth:{access_token}\n".encode('utf-8')) 
        irc.send(f"NICK {bot_username}\n".encode('utf-8'))
        irc.send(f"JOIN #{channel_name}\n".encode('utf-8'))

        print(f"Connected to {channel_name}'s chat as {bot_username}")
        return irc
    print("Failed to validate token. Exiting.")
