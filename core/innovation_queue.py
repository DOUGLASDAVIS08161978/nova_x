#!/usr/bin/env python3
"""
===========================================================
NOVA-X Innovation Queue v1.0
===========================================================

Stores capability ideas and engineering improvements.

Author:
Douglas Davis & OpenAI
===========================================================
"""

import json
import os
from datetime import datetime


class InnovationQueue:

    def __init__(self, filename="innovation_queue.json"):

        self.filename = filename

        if not os.path.exists(filename):

            with open(filename, "w") as f:

                json.dump([], f, indent=4)

    def _load(self):

        with open(self.filename, "r") as f:

            return json.load(f)

    def _save(self, queue):

        with open(self.filename, "w") as f:

            json.dump(queue, f, indent=4)

    def add(
        self,
        title,
        description,
        priority="Medium"
    ):

        queue = self._load()

        item = {

            "created": datetime.now().isoformat(timespec="seconds"),

            "title": title,

            "description": description,

            "priority": priority,

            "status": "Pending"

        }

        queue.append(item)

        self._save(queue)

        return item

    def list_items(self):

        return self._load()

    def show(self):

        queue = self._load()

        print()

        print("=" * 60)
        print("NOVA-X INNOVATION QUEUE")
        print("=" * 60)

        print()

        if not queue:

            print("Innovation Queue Empty.")
            return

        for i, item in enumerate(queue, 1):

            print(f"{i}.")

            print(" Title      :", item["title"])

            print(" Priority   :", item["priority"])

            print(" Status     :", item["status"])

            print(" Description:")

            print("  ", item["description"])

            print()


############################################################

if __name__ == "__main__":

    queue = InnovationQueue()

    queue.add(

        "PDF Reader",

        "Design and implement a tool capable of extracting searchable text from PDF documents.",

        "High"

    )

    queue.add(

        "Image Analyzer",

        "Investigate adding image understanding capabilities.",

        "Medium"

    )

    queue.show()
