#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
NOVA X GOAL MANAGER v1.0
Persistent Engineering Mission
═══════════════════════════════════════════════════════════════════════

Purpose:
    Maintain long-term engineering objectives.

This module NEVER edits source code.
It only decides what Nova should work on next.
"""

from pathlib import Path
from datetime import datetime, UTC
import json

REPORT_DIR = Path("self_evolution/reports")

PLAN = REPORT_DIR / "improvement_plan.json"
OUTPUT = REPORT_DIR / "active_goal.json"


MISSION = """
Continuously improve the reliability,
maintainability,
performance,
security,
test coverage,
documentation,
and reasoning capability
of Nova X while preserving
human approval for every code change.
""".strip()


class GoalManager:

    def __init__(self):
        self.plan = None

    def load_plan(self):

        with open(PLAN, "r", encoding="utf-8") as f:
            self.plan = json.load(f)

    def choose_goal(self):

        tasks = sorted(
            self.plan["tasks"],
            key=lambda t: (
                t["priority"],
                t["confidence"]
            ),
            reverse=True
        )

        goal = tasks[0]

        return {
            "generated": datetime.now(UTC).isoformat(),
            "mission": MISSION,
            "selected_goal": goal["title"],
            "priority": goal["priority"],
            "confidence": goal["confidence"],
            "risk": goal["risk"],
            "estimated_effort": goal["estimated_effort"],
            "reason": goal["reason"],
            "next_action": goal["next_action"],
            "status": "Awaiting Human Approval",
            "may_modify_code": False,
            "human_review_required": True
        }

    def save(self):

        self.load_plan()

        goal = self.choose_goal()

        with open(
            OUTPUT,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                goal,
                f,
                indent=4
            )

        return goal


def main():
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""

    if not PLAN.exists():

        print("Missing improvement plan.")
        print("Run:")
        print("python3 self_evolution/improvement_planner.py")
        return

    manager = GoalManager()

    goal = manager.save()

    print()
    print("=" * 60)
    print("NOVA X ACTIVE ENGINEERING GOAL")
    print("=" * 60)
    print()

    print("Mission:")
    print(goal["mission"])
    print()

    print("Current Goal:")
    print(goal["selected_goal"])
    print()

    print(f"Priority   : {goal['priority']}")
    print(f"Confidence : {goal['confidence']:.2f}")
    print(f"Risk       : {goal['risk']}")
    print(f"Effort     : {goal['estimated_effort']}")
    print()

    print("Status:")
    print(goal["status"])
    print()

    print("Saved:")
    print(OUTPUT)


if __name__ == "__main__":
    main()

