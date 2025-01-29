""" This Test Module Tests the functions in the main.py file """
import json
import pytest
from main import main, load_commands


def test_load_commands(tmp_path):
    """ Test the load_commands function """
    commands = {"!command": "response"}
    file_path = tmp_path / "commands.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(commands, file)

    result = load_commands(file_path)
    assert result == commands

def test_load_commands_file_not_found():
    """ Test the load_commands function when the file is not found """
    with pytest.raises(FileNotFoundError):
        load_commands("non_existent_file.json")

def test_main(mock_load_commands, mock_connect_twitch_chat, mock_manage_chat_connection, capsys):
    """ Test the main function """
    main()
    captured = capsys.readouterr()
    access_token = "test_access_token"
    client_id = "test_client_id"
    bot_username = "test_bot_username"
    channel_name = "test_channel_name"
    irc = mock_connect_twitch_chat.return_value
    commands = mock_load_commands.return_value

    assert mock_load_commands.calledwith("../config/commands.json")
    assert mock_connect_twitch_chat.calledwith(access_token, client_id, bot_username, channel_name)
    assert mock_manage_chat_connection.calledwith(irc, bot_username, channel_name, commands)
    assert "END" in captured.out
