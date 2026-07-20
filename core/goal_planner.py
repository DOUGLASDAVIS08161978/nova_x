#!/usr/bin/env python3
"""
============================================================
NOVA-X Goal Planner v1.0
============================================================

Transforms a high-level goal into an executable plan.

Douglas Davis & OpenAI
============================================================
"""

from datetime import datetime
import json
from pathlib import Path

PLAN_LOG = Path("goal_plans.json")


class GoalPlanner:

    def __init__(self):
        self.timestamp = datetime.now().isoformat(timespec="seconds")

    def create_plan(self, goal):

        goal_lower = goal.lower()

        if "battery" in goal_lower:

            steps = [
                "Collect observations",
                "Generate competing hypotheses",
                "Determine the most likely explanation",
                "Design diagnostic tests",
                "Execute tests",
                "Reflect on results",
                "Store lessons learned"
            ]

        elif "code" in goal_lower or "module" in goal_lower:

            steps = [
                "Analyze requirements",
                "Design architecture",
                "Implement solution",
                "Run tests",
                "Reflect on implementation",
                "Store improvements"
            ]

        else:

            steps = [
                "Understand objective",
                "Break goal into subgoals",
                "Prioritize actions",
                "Execute tasks",
                "Evaluate outcome",
                "Reflect",
                "Store knowledge"
            ]

        return {
            "timestamp": self.timestamp,
            "goal": goal,
            "steps": steps,
            "status": "planned"
        }

    def save_plan(self, plan):

        history = []

        if PLAN_LOG.exists():

            try:
                history = json.loads(PLAN_LOG.read_text())
            except Exception:
                history = []

        history.append(plan)

        PLAN_LOG.write_text(
            json.dumps(history, indent=4)
        )

    def print_plan(self, plan):

        print()
        print("=" * 60)
        print("NOVA-X GOAL PLAN")
        print("=" * 60)
        print()

        print("Goal:")
        print(plan["goal"])
        print()

        print("Execution Plan:")

        for i, step in enumerate(plan["steps"], start=1):
            print(f" {i}. {step}")

        print()
        print("Status:", plan["status"])
        print("=" * 60)


############################################################

if __name__ == "__main__":

    planner = GoalPlanner()

    plan = planner.create_plan(
        "Design an intelligent e-bike battery diagnostic module."
    )

    planner.save_plan(plan)

    planner.print_plan(plan)

    print()
    print("Goal plan saved to goal_plans.json")
