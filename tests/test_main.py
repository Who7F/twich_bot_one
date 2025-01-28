""" This Test Module Tests the functions in the main.py file """
import json
import pytest
from src.main import main, load_commands


def test_load_commands(tmp_path):
    commands = {"!command": "response"}
    file_path = tmp_path / "commands.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(commands, file)

    result = load_commands(file_path)
    assert result == commands

def test_load_commands_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_commands("non_existent_file.json")

def test_main(mock_load_commands, mock_connect_twitch_chat, mock_manage_chat_connection, capsys):
    main()
    captured = capsys.readouterr()
    assert mock_load_commands.calledwith("../config/commands.json")
    assert mock_connect_twitch_chat.calledwith("test_access_token", "test_client_id", "test_bot_username", "test_channel_name")
    assert mock_manage_chat_connection.calledwith(mock_connect_twitch_chat.return_value, "test_bot_username", "test_channel_name", mock_load_commands.return_value)
    assert "END" in captured.out
