#!/usr/bin/env python3

"""
NOVA-X Plugin Manager
Version 0.1
"""

import os


class PluginManager:

    def __init__(self, plugin_directory="plugins"):
        self.plugin_directory = plugin_directory
        self.plugins = []

    def discover(self):

        self.plugins.clear()

        if not os.path.exists(self.plugin_directory):
            print("[PluginManager] Plugin directory not found.")
            return

        for filename in sorted(os.listdir(self.plugin_directory)):

            if filename.endswith(".py") and not filename.startswith("__"):
                self.plugins.append(filename[:-3])

        print(f"[PluginManager] Found {len(self.plugins)} plugin(s).")

    def list_plugins(self):

        if not self.plugins:
            print("[PluginManager] No plugins loaded.")
            return

        print("\nLoaded Plugins")

        for plugin in self.plugins:
            print(f"  ✓ {plugin}")

    def update(self):

        print(f"[PluginManager] Monitoring {len(self.plugins)} plugin(s).")


if __name__ == "__main__":

    manager = PluginManager()

    manager.discover()

    manager.list_plugins()

    manager.update()
