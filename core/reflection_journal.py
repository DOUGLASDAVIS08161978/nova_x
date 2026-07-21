#!/usr/bin/env python3
"""
===========================================================
NOVA-X Reflection Journal v1.0
===========================================================

Stores self-reflections and lessons learned.

Each reflection contains:
- Timestamp
- Topic
- Reflection
- Priority

Future versions:
- Pattern detection
- Goal generation
- Automatic improvement suggestions
===========================================================
"""

import json
from datetime import datetime
from pathlib import Path

REFLECTION_FILE = Path.home() / "nova_x" / "memory" / "reflections.json"


class ReflectionJournal:

    def __init__(self):

        REFLECTION_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not REFLECTION_FILE.exists():
            REFLECTION_FILE.write_text("[]")

        self.load()

    def load(self):

        try:

            with open(REFLECTION_FILE, "r") as f:
                self.reflections = json.load(f)

        except Exception:
            self.reflections = []

    def save(self):

        with open(REFLECTION_FILE, "w") as f:

            json.dump(
                self.reflections,
                f,
                indent=2
            )

    def add(self, topic, reflection, priority="normal"):

        self.reflections.append({

            "timestamp": str(datetime.now()),
            "topic": topic,
            "priority": priority,
            "reflection": reflection

        })

        self.save()

    def latest(self, count=5):

        return self.reflections[-count:]

    def summary(self):

        if not self.reflections:
            return "No reflections recorded."

        lines = []

        for item in self.latest():

            lines.append(
                f"[{item['timestamp']}] "
                f"{item['topic']} "
                f"({item['priority']})"
            )

        return "\n".join(lines)


if __name__ == "__main__":

    journal = ReflectionJournal()

    journal.add(

        topic="Startup",

        reflection=(
            "Reflection Journal installed successfully."
        ),

        priority="high"

    )

    print()
    print("=" * 55)
    print("NOVA-X REFLECTION JOURNAL")
    print("=" * 55)
    print()

    print(journal.summary())
