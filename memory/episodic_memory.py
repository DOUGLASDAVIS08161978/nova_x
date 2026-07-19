#!/usr/bin/env python3
"""
===========================================================
NOVA-X Episodic Memory Engine v1.0
===========================================================

Persistent experience storage.

Stores:
- timestamp
- event
- engine
- prompt
- response
- success
- metadata

Future versions:
- semantic search
- importance scoring
- clustering
- memory consolidation
===========================================================
"""

import json
from pathlib import Path
from datetime import datetime


class EpisodicMemory:

    def __init__(self,
                 filename="data/episodic_memory.json"):

        self.file = Path(filename)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.memories = []

        self.load()


    def load(self):

        if self.file.exists():

            try:

                with open(self.file, "r") as f:

                    self.memories = json.load(f)

            except Exception:

                self.memories = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                self.memories,
                f,
                indent=2
            )


    def remember(
        self,
        event,
        prompt="",
        response="",
        engine="",
        success=True,
        metadata=None
    ):

        if metadata is None:
            metadata = {}

        memory = {

            "timestamp":
                str(datetime.now()),

            "event":
                event,

            "engine":
                engine,

            "prompt":
                prompt,

            "response":
                response,

            "success":
                success,

            "metadata":
                metadata

        }

        self.memories.append(memory)

        self.save()

        return memory


    def recent(self, count=5):

        return self.memories[-count:]


    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for memory in self.memories:

            text = json.dumps(memory).lower()

            if keyword in text:

                results.append(memory)

        return results


    def summary(self):

        successful = sum(
            1 for m in self.memories
            if m["success"]
        )

        failed = len(self.memories) - successful

        engines = {}

        for m in self.memories:

            engine = m.get("engine", "unknown")

            engines[engine] = engines.get(engine, 0) + 1

        return {

            "total_memories":
                len(self.memories),

            "successful":
                successful,

            "failed":
                failed,

            "engines":
                engines

        }


if __name__ == "__main__":

    memory = EpisodicMemory()

    memory.remember(

        event="reasoning",

        prompt="Explain modular AI.",

        response="Example response.",

        engine="groq",

        success=True

    )

    print()

    print("Summary")

    print(memory.summary())

    print()

    print("Recent Memories")

    for item in memory.recent():

        print("-" * 40)
        print(item)
