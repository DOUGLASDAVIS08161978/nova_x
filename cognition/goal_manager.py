#!/usr/bin/env python3
"""
===========================================================
NOVA-X Goal Manager v1.0
===========================================================

Manages objectives, priorities, and progress tracking.

Features:
- Create goals
- Update progress
- Prioritize objectives
- Track completion
- Persist goals to disk

Future:
- Goal decomposition
- Planning integration
- Reward modeling
- Long-term strategy
===========================================================
"""

import json
from pathlib import Path
from datetime import datetime
import uuid


class GoalManager:

    def __init__(self,
                 filename="data/goals.json"):

        self.file = Path(filename)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.goals = []

        self.load()


    def load(self):

        if self.file.exists():

            try:

                with open(self.file, "r") as f:

                    self.goals = json.load(f)

            except Exception:

                self.goals = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                self.goals,
                f,
                indent=2
            )


    def create_goal(
        self,
        title,
        description,
        priority="Medium"
    ):

        goal = {

            "id":
                str(uuid.uuid4()),

            "created":
                str(datetime.now()),

            "title":
                title,

            "description":
                description,

            "priority":
                priority,

            "progress":
                0,

            "status":
                "Active"

        }

        self.goals.append(goal)

        self.save()

        return goal


    def update_progress(
        self,
        goal_id,
        progress
    ):

        for goal in self.goals:

            if goal["id"] == goal_id:

                goal["progress"] = progress

                if progress >= 100:

                    goal["status"] = "Complete"

                self.save()

                return goal

        return None


    def active_goals(self):

        return [

            g for g in self.goals

            if g["status"] == "Active"

        ]


    def summary(self):

        return {

            "total":
                len(self.goals),

            "active":
                len(self.active_goals())

        }


if __name__ == "__main__":

    manager = GoalManager()


    goal = manager.create_goal(

        "Improve NOVA-X Architecture",

        "Expand cognitive modules and improve integration.",

        priority="High"

    )


    print("\nCreated Goal:\n")

    print(goal)


    print("\nSummary:\n")

    print(
        manager.summary()
    )
