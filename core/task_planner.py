#!/usr/bin/env python3
"""
===========================================================
NOVA-X Task Planner v1.0
===========================================================

Creates structured execution plans for NOVA-X.

Author:
Douglas Davis & OpenAI

===========================================================
"""


class TaskPlanner:

    def __init__(self, registry):
        self.registry = registry

    def create_plan(self, goal):

        goal_lower = goal.lower()

        steps = []

        if "python" in goal_lower or "code" in goal_lower:
            if self.registry.has("Code Executor"):
                steps.append(
                    "Use Code Executor to execute Python."
                )

        if "experiment" in goal_lower:
            if self.registry.has("Experiment Engine"):
                steps.append(
                    "Run controlled experiment."
                )

        if (
            "github" in goal_lower
            or "browser" in goal_lower
            or "website" in goal_lower
        ):
            if self.registry.has("Android Agent"):
                steps.append(
                    "Open browser using Android Agent."
                )

        if not steps:
            steps.append(
                "Reason about the request."
            )

        return {

            "goal": goal,

            "steps": steps,

            "step_count": len(steps)

        }


###############################################################

if __name__ == "__main__":

    from tool_registry import ToolRegistry

    class Dummy:
        pass

    registry = ToolRegistry()

    registry.register(
        "Code Executor",
        Dummy()
    )

    registry.register(
        "Experiment Engine",
        Dummy()
    )

    registry.register(
        "Android Agent",
        Dummy()
    )

    planner = TaskPlanner(registry)

    plan = planner.create_plan(

        "Run a Python experiment then open GitHub"

    )

    print()

    print("=" * 55)
    print("TASK PLAN")
    print("=" * 55)

    print()

    print("Goal:")

    print(plan["goal"])

    print()

    print("Steps:")

    for i, step in enumerate(plan["steps"], 1):

        print(f"{i}. {step}")

    print()

