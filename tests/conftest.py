"""This ia the Pytest configuration file for the project."""

import os
import sys
import pytest
from pathlib import Path

from dotenv import load_dotenv

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

# Load the environment variables from the test.env file
def pytest_configure(config):
    """ This is run before any imports allowing us to inject
    dependencies via environment variables into Settings
    This just affects the variables in this process's environment

    Find the .env file for the test environment"""

    test_env = str("test.env")

    # Load the environment variables and overwrite any existing ones
    load_dotenv(test_env, override=True)



@pytest.fixture
def mock_load_commands(mocker):
    return mocker.patch("main.load_commands", return_value={"!command": "response"})

@pytest.fixture
def mock_connect_twitch_chat(mocker):
    return mocker.patch("main.connect_twitch_chat", return_value=True)

@pytest.fixture
def mock_manage_chat_connection(mocker):
    return mocker.patch("main.manage_chat_connection")
