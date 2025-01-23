from dotenv import load_dotenv

def pytest_configure(config):
    # This is run before any imports allowing us to inject
    # dependencies via environment variables into Settings
    # This just affects the variables in this process's environment

    # Find the .env file for the test environment
    test_env = str("test.env")
    # Load the environment variables and overwrite any existing ones
    load_dotenv(test_env, override=True)