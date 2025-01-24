""" This Test Module Tests the functions in the main.py file """
import pytest
import json
from unittest import mock
from src.main import main, load_commands

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN", "oauth:test_access_token")
    monkeypatch.setenv("CLIENT_ID", "test_client_id")
    monkeypatch.setenv("BOT_USERNAME", "test_bot_username")
    monkeypatch.setenv("CHANNEL_NAME", "test_channel_name")

@pytest.fixture
def mock_load_commands():
    with mock.patch("main.load_commands") as mock_load:
        mock_load.return_value = {"!command": "response"}
        yield mock_load

@pytest.fixture
def mock_connect_twitch_chat():
    with mock.patch("main.connect_twitch_chat") as mock_connect:
        mock_connect.return_value = True
        yield mock_connect

@pytest.fixture
def mock_manage_chat_connection():
    with mock.patch("main.manage_chat_connection") as mock_manage:
        yield mock_manage
        
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

def test_main(mock_env_vars, mock_load_commands, mock_connect_twitch_chat, mock_manage_chat_connection, capsys):
    main()
    captured = capsys.readouterr()
    assert "remove oauth: form ACCESS_TOKEN" in captured.out
    assert mock_load_commands.called
    assert mock_connect_twitch_chat.called
    assert mock_manage_chat_connection.called
    assert "END" in captured.out

def test_main_failed_connection(mock_env_vars, mock_load_commands, capsys):
    with mock.patch("main.connect_twitch_chat", return_value=False):
        main()
        captured = capsys.readouterr()
        assert "Failed Relay Chat. Exiting." in captured.out
        assert "END" in captured.out
