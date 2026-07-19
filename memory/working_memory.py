#!/usr/bin/env python3

"""
NOVA-X Working Memory
Version 0.1
"""

from datetime import datetime


class WorkingMemory:

    def __init__(self):
        self.memory = []

    def add(self, item):
        self.memory.append({
            "time": datetime.now(),
            "content": item
        })

    def recall(self):
        return self.memory

    def clear(self):
        self.memory.clear()

    def update(self):
        print(f"[WorkingMemory] {len(self.memory)} items stored.")


if __name__ == "__main__":

    wm = WorkingMemory()

    wm.add("System Booted")

    wm.add("Executive Controller Online")

    wm.update()

    print()

    for item in wm.recall():
        print(item["time"], "-", item["content"])
