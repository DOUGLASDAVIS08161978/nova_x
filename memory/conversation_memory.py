#!/usr/bin/env python3
"""
===========================================================
NOVA-X Conversation Memory v1.0
===========================================================

Stores the current conversation.

Features
--------
- Stores user messages
- Stores NOVA-X replies
- Saves automatically
- Retrieves recent history
- Ready for Reasoning Manager integration

===========================================================
"""

import json
from pathlib import Path
from datetime import datetime


class ConversationMemory:

    def __init__(self,
                 filename="data/conversation_memory.json"):

        self.file = Path(filename)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.history = []

        self.load()


    def load(self):

        if self.file.exists():

            try:

                with open(self.file, "r") as f:

                    self.history = json.load(f)

            except Exception:

                self.history = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(

                self.history,

                f,

                indent=2

            )


    def remember(self,
                 speaker,
                 message):

        self.history.append({

            "time": str(datetime.now()),

            "speaker": speaker,

            "message": message

        })

        self.save()


    def recent(self,
               limit=10):

        return self.history[-limit:]


    def context(self,
                limit=10):

        lines = []

        for item in self.recent(limit):

            lines.append(

                f"{item['speaker']}: {item['message']}"

            )

        return "\n".join(lines)


    def clear(self):

        self.history = []

        self.save()


    def stats(self):

        return {

            "messages": len(self.history)

        }


if __name__ == "__main__":

    memory = ConversationMemory()

    memory.remember(

        "Douglas",

        "Hello NOVA."

    )

    memory.remember(

        "NOVA-X",

        "Hello Douglas! Nice to see you."

    )

    print()

    print("Conversation Memory")

    print("-------------------")

    print(memory.context())

    print()

    print(memory.stats())
