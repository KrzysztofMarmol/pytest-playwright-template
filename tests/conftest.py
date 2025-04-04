import pytest
from faker import Faker
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def faker_instance():
    """Provides a Faker instance for generating test data."""
    return Faker()


@pytest.fixture(scope="session")
def test_config() -> dict:
    """Loads and parses test credentials from the TEST_CREDENTIALS_JSON env var."""
    creds_json_str = os.getenv("TEST_CREDENTIALS_JSON")
    if not creds_json_str:
        return {}
    try:
        credentials = json.loads(creds_json_str)
        return credentials
    except json.JSONDecodeError:
        pytest.fail(
            f"Failed to parse JSON from TEST_CREDENTIALS_JSON: {creds_json_str}"
        )


@pytest.fixture(scope="session")
def base_url() -> str:
    """Provides the base URL from the BASE_URL environment variable.
    
    This fixture overrides the --base-url command line argument from pytest-playwright."""
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def device() -> str:
    """Provides the device from the DEVICE environment variable.
    
    This fixture overrides the --device command line argument from pytest-playwright."""
    return os.getenv("DEVICE")