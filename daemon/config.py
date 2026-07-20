"""
═══════════════════════════════════════════════════════════════════════
NOVA-X DAEMON CONFIGURATION
═══════════════════════════════════════════════════════════════════════
"""

import json
from pathlib import Path

CONFIG_FILE = Path("config/daemon_config.json")


DEFAULT_CONFIG = {
    "daemon": {
        "enabled": True,
        "sleep_interval": 10,
        "heartbeat_interval": 60,
        "auto_start": True,
        "debug": False
    },

    "research": {
        "enabled": True,
        "max_cycles": 5
    },

    "reflection": {
        "enabled": True
    },

    "journal": {
        "enabled": True
    },

    "missions": {
        "enabled": True
    },

    "plugins": {
        "enabled": True,
        "directory": "plugins"
    }
}


class ConfigManager:

    def __init__(self):
        self.config = {}

    def load(self):

        if not CONFIG_FILE.exists():
            self.config = DEFAULT_CONFIG
            self.save()
            return self.config

        with open(CONFIG_FILE, "r") as f:
            self.config = json.load(f)

        return self.config

    def save(self):

        CONFIG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(CONFIG_FILE, "w") as f:
            json.dump(
                self.config,
                f,
                indent=4
            )

    def get(self, *keys, default=None):

        value = self.config

        for key in keys:

            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value

    def set(self, value, *keys):

        current = self.config

        for key in keys[:-1]:

            if key not in current:
                current[key] = {}

            current = current[key]

        current[keys[-1]] = value

        self.save()


config = ConfigManager()
config.load()


if __name__ == "__main__":

    print("═══════════════════════════")
    print("NOVA-X Configuration")
    print("═══════════════════════════")

    print(json.dumps(
        config.config,
        indent=4
    ))
