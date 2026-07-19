#!/usr/bin/env python3
"""
===========================================================
NOVA-X Global Workspace v2.0
===========================================================

Shared cognitive workspace.

Features
--------
- Backward compatible broadcast()
- Categories
- Priority
- Confidence
- Metadata
- Filtering
- Statistics

===========================================================
"""

from datetime import datetime


class GlobalWorkspace:

    def __init__(self):

        self.workspace = []


    def broadcast(
        self,
        source,
        message,
        category="general",
        priority=0.50,
        confidence=1.00,
        metadata=None
    ):

        event = {

            "time": datetime.now(),

            "source": source,

            "category": category,

            "priority": float(priority),

            "confidence": float(confidence),

            "message": message,

            "metadata": metadata or {}

        }

        self.workspace.append(event)

        print(
            f"[Workspace] "
            f"{source} "
            f"({category}) "
            f"{message}"
        )

        return event


    def get_events(self):

        return list(self.workspace)


    def get_category(
        self,
        category
    ):

        return [

            e for e in self.workspace

            if e["category"] == category

        ]


    def get_high_priority(
        self,
        threshold=0.80
    ):

        return [

            e for e in self.workspace

            if e["priority"] >= threshold

        ]


    def recent(
        self,
        count=10
    ):

        return self.workspace[-count:]


    def clear(self):

        self.workspace.clear()


    def stats(self):

        categories = {}

        for event in self.workspace:

            cat = event["category"]

            categories[cat] = categories.get(cat, 0) + 1

        return {

            "events": len(self.workspace),

            "categories": categories

        }


    def update(self):

        s = self.stats()

        print()

        print("========== Workspace ==========")

        print("Events:", s["events"])

        print("Categories:")

        for name, count in s["categories"].items():

            print(f"  {name}: {count}")

        print("===============================")


if __name__ == "__main__":

    gw = GlobalWorkspace()

    gw.broadcast(

        "Memory",

        "Boot Complete"

    )

    gw.broadcast(

        "Reasoner",

        "Prices will rise.",

        category="prediction",

        priority=0.90,

        confidence=0.88,

        metadata={

            "domain": "market"

        }

    )

    gw.broadcast(

        "Planner",

        "Research task created.",

        category="goal",

        priority=0.70

    )

    print()

    print("Recent:")

    for event in gw.recent():

        print(event)

    print()

    gw.update()
