import json
import os

CREDENTIALS_PATH = os.path.expanduser("~/.data-retrival-agent/credentials.json")


def load_credentials():
    """Return credentials needed for the tool to work."""
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH) as f:
            return json.load(f)
    return {}


def save_credentials(data):
    """Save credentials to ~/.data-retrival-agent/config.json"""
    os.makedirs(os.path.dirname(CREDENTIALS_PATH), exist_ok=True)
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump(data, f, indent=2)
