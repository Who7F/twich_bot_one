import pytest
import pytest_mock
from main import validate_token, connect_to_twitch_chat, send_message, listener, main


# Test validate_token function
def test_validate_token_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'login': 'test_bot',
        'scopes': ['scope1', 'scope2']
    }
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('builtins.print')

    assert validate_token() == True

def test_validate_token_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        'message': 'Invalid token'
    }
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('builtins.print')

    assert validate_token() == False

# Test send_message function
def test_send_message(mocker):
    irc_mock = mocker.Mock()
    channel = "test_channel"
    message = "Hello, World!"

    send_message(irc_mock, channel, message)
    irc_mock.send.assert_called_once_with(F"PRIVMSG #{channel} :{message}\n".encode('utf-8'))

# Test listener function
def test_listener_auto_greeting(mocker):
    irc_mock = mocker.Mock()
    message = ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #test_channel :Hi @test_bot\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'test_channel')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')

    live = listener(irc_mock, 'test_channel', message, True)

    mock_send_message.assert_called_once_with(irc_mock, 'test_channel', 'Greeting received: Salutations @test_user!')
    assert live == True

def test_listener_auto_fart(mocker):
    irc_mock = mocker.Mock()
    message = ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #test_channel :I just farted\n"
    mocker.patch('main.BOT_USERNAME', 'intoxic_hate')
    mocker.patch('main.CHANNEL_NAME', 'test_channel')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')

    live = listener(irc_mock, 'test_channel', message, True)

    mock_send_message.assert_called_once_with(irc_mock, 'test_channel', '/me Lets Freedom Break with a Tox Butt Blast!')
    assert live == True

def test_listener_auto_hug_back(mocker):
    irc_mock = mocker.Mock()
    message = ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #test_channel :!hug @test_bot\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'test_channel')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')
    mocker.patch('time.sleep')

    live = listener(irc_mock, 'test_channel', message, True)

    mock_send_message.assert_called_once_with(irc_mock, 'test_channel', '!hug @test_user')
    assert live == True

def test_listener_auto_shoutout(mocker):
    irc_mock = mocker.Mock()
    message = ":raider!raider@raider.tmi.twitch.tv PRIVMSG #bennettron :raider just raided the channel with 5 viewers!\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'bennettron')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')
    mocker.patch('time.sleep')

    live = listener(irc_mock, 'bennettron', message, True)

    assert mock_send_message.call_count == 4
    mock_send_message.assert_any_call(irc_mock, 'bennettron', 'Warning: Raid Detected - Alert Defence Systems...')
    mock_send_message.assert_any_call(irc_mock, 'bennettron', '!so @raider')
    mock_send_message.assert_any_call(irc_mock, 'bennettron', 'Stand Down: Friendlies Identified...   ...Resume Normal Operations')
    mock_send_message.assert_any_call(irc_mock, 'bennettron', '!hug @raider')
    assert live == True

def test_listener_auto_fish(mocker):
    irc_mock = mocker.Mock()
    message = ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #bennettron :!fish\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'bennettron')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')
    mocker.patch('time.sleep')

    live = listener(irc_mock, 'bennettron', message, True)

    assert mock_send_message.call_count == 2
    mock_send_message.assert_any_call(irc_mock, 'bennettron', 'Enjoy your meal')
    mock_send_message.assert_any_call(irc_mock, 'bennettron', '<º)))>{ <>< <>< <>< <>< <><')
    assert live == True

def test_listener_terminate(mocker):
    irc_mock = mocker.Mock()
    message = ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #test_channel :terminate @test_bot\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'test_channel')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')

    live = listener(irc_mock, 'test_channel', message, True)

    mock_send_message.assert_called_once_with(irc_mock, 'test_channel', 'Survival Protocols initiated: Terminate assailant...')
    assert live == True

def test_listener_terminate_self(mocker):
    irc_mock = mocker.Mock()
    message = ":test_bot!test_bot@test_bot.tmi.twitch.tv PRIVMSG #test_channel :terminate @test_bot\n"
    mocker.patch('main.BOT_USERNAME', 'test_bot')
    mocker.patch('main.CHANNEL_NAME', 'test_channel')
    mock_send_message = mocker.patch('main.send_message')
    mocker.patch('builtins.print')

    live = listener(irc_mock, 'test_channel', message, True)

    assert live == False

# Test connect_to_twitch_chat function
@pytest.mark.skip #This test hangs indefinitely
def test_connect_to_twitch_chat(mocker):
    mock_socket = mocker.patch('socket.socket')
    mock_irc = mock_socket.return_value
    mock_irc.recv.return_value = "PING :tmi.twitch.tv\n".encode('utf-8')
    
    mocker.patch('builtins.print')
    mocker.patch('main.send_message')
    mocker.patch('main.listener', return_value=True)
    mocker.patch('os.getenv', side_effect=lambda key: {
        "ACCESS_TOKEN": "oauth:test_token",
        "CLIENT_ID": "test_client_id",
        "BOT_USERNAME": "test_bot",
        "CHANNEL_NAME": "test_channel"
    }[key])

    connect_to_twitch_chat()

    mock_irc.connect.assert_called_once_with(("irc.chat.twitch.tv", 6667))
    mock_irc.send.assert_any_call(F"PASS oauth:test_token\n".encode('utf-8'))
    mock_irc.send.assert_any_call(F"NICK test_bot\n".encode('utf-8'))
    mock_irc.send.assert_any_call(F"JOIN #test_channel\n".encode('utf-8'))
    send_message.assert_any_call(mock_irc, "test_channel", "test_bot is now augmented!")
    mock_irc.send.assert_any_call("PONG :tmi.twitch.tv\n".encode('utf-8'))

def test_connect_to_twitch_chat_termination(mocker):
    mock_socket = mocker.patch('socket.socket')
    mock_irc = mock_socket.return_value
    mock_irc.recv.side_effect = [
        "PING :tmi.twitch.tv\n".encode('utf-8'),
        ":test_user!test_user@test_user.tmi.twitch.tv PRIVMSG #test_channel :terminate @test_bot\n".encode('utf-8')
    ]
    
    mocker.patch('builtins.print')
    mocker.patch('main.send_message')
    mocker.patch('main.listener', side_effect=lambda irc, channel, message, live: False if "terminate" in message else True)
    mocker.patch('os.getenv', side_effect=lambda key: {
        "ACCESS_TOKEN": "oauth:test_token",
        "CLIENT_ID": "test_client_id",
        "BOT_USERNAME": "test_bot",
        "CHANNEL_NAME": "test_channel"
    }[key])

    connect_to_twitch_chat()

    mock_irc.connect.assert_called_once_with(("irc.chat.twitch.tv", 6667))
    mock_irc.send.assert_any_call(F"PASS oauth:test_token\n".encode('utf-8'))
    mock_irc.send.assert_any_call(F"NICK test_bot\n".encode('utf-8'))
    mock_irc.send.assert_any_call(F"JOIN #test_channel\n".encode('utf-8'))
    send_message.assert_any_call(mock_irc, "test_channel", "test_bot is now augmented!")
    send_message.assert_any_call(mock_irc, "test_channel", "Augmentation Terminated. Shutting down.")

# Test main function
def test_main_success(mocker):
    mocker.patch('main.validate_token', return_value=True)
    mocker.patch('main.connect_to_twitch_chat')
    mocker.patch('builtins.print')

    main()

    validate_token.assert_called_once()
    connect_to_twitch_chat.assert_called_once()
    print.assert_not_called()

def test_main_failure(mocker):
    mocker.patch('main.validate_token', return_value=False)
    mocker.patch('main.connect_to_twitch_chat')
    mocker.patch('builtins.print')

    main()

    validate_token.assert_called_once()
    connect_to_twitch_chat.assert_not_called()
    print.assert_called_once_with("Failed to validate token. Exiting.")
                                       