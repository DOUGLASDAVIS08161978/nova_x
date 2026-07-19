#!/usr/bin/env python3

"""
NOVA-X Global Workspace
Version 0.1
"""

from datetime import datetime


class GlobalWorkspace:

    def __init__(self):
        self.workspace = []

    def broadcast(self, source, message):

        event = {
            "time": datetime.now(),
            "source": source,
            "message": message
        }

        self.workspace.append(event)

        print(f"[Workspace] {source}: {message}")

    def get_events(self):
        return self.workspace

    def clear(self):
        self.workspace.clear()

    def update(self):
        print(f"[Workspace] {len(self.workspace)} active events")


if __name__ == "__main__":

    gw = GlobalWorkspace()

    gw.broadcast("Memory", "System Boot Complete")

    gw.broadcast("Planner", "Waiting For Tasks")

    gw.broadcast("Identity", "Initializing Self Model")

    print()

    for event in gw.get_events():
        print(event["time"], "-", event["source"], "-", event["message"])
