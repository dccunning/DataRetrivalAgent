import json
import os

CONFIG_PATH = os.path.expanduser("~/.data-retrival-agent/config.json")


def load_config():
    """Return credentials needed for the tool to work."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def save_config(data):
    """Save credentials to ~/.data-retrival-agent/config.json"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
