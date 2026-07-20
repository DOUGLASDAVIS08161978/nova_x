#!/usr/bin/env python3
"""
===========================================================
NOVA-X Action Planner v1.0
===========================================================

Transforms a high-level goal into an ordered execution plan.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from datetime import datetime


class ActionPlanner:

    def __init__(self):

        self.created = datetime.now().isoformat(timespec="seconds")

    def create_plan(self, goal):

        return [

            {
                "step": 1,
                "title": "Understand Goal",
                "status": "PENDING"
            },

            {
                "step": 2,
                "title": "Analyze Required Capabilities",
                "status": "PENDING"
            },

            {
                "step": 3,
                "title": "Generate Solution Strategy",
                "status": "PENDING"
            },

            {
                "step": 4,
                "title": "Execute Tasks",
                "status": "PENDING"
            },

            {
                "step": 5,
                "title": "Evaluate Results",
                "status": "PENDING"
            },

            {
                "step": 6,
                "title": "Record Knowledge",
                "status": "PENDING"
            }

        ]

    def print_plan(self, goal, plan):

        print()
        print("=" * 60)
        print("NOVA-X ACTION PLAN")
        print("=" * 60)
        print()

        print(f"GOAL: {goal}")
        print()

        for item in plan:

            print(
                f"[{item['step']}] "
                f"{item['title']} "
                f"({item['status']})"
            )

        print()


############################################################

if __name__ == "__main__":

    planner = ActionPlanner()

    goal = "Create a PDF Reader"

    plan = planner.create_plan(goal)

    planner.print_plan(goal, plan)
