#!/usr/bin/env python3
"""
===========================================================
NOVA-X Task Executor v1.1
===========================================================
"""

from datetime import datetime
from tool_registry import ToolRegistry
from task_planner import TaskPlanner


class DummyTool:

    def __init__(self, name):
        self.name = name

    def run(self):
        return f"{self.name} completed successfully."


class TaskExecutor:

    def __init__(self, registry):
        self.registry = registry

    def _select_tool(self, step):

        s = step.lower()

        if "code executor" in s or "python" in s or "execute python" in s:
            return self.registry.get("Code Executor")

        if "experiment" in s:
            return self.registry.get("Experiment Engine")

        if "android" in s or "browser" in s or "github" in s:
            return self.registry.get("Android Agent")

        return None

    def execute(self, plan):

        report = {
            "goal": plan["goal"],
            "started": datetime.now().isoformat(timespec="seconds"),
            "results": []
        }

        for step in plan["steps"]:

            tool = self._select_tool(step)

            if tool:

                result = tool.run()

                report["results"].append({
                    "step": step,
                    "status": "SUCCESS",
                    "outcome": result
                })

            else:

                report["results"].append({
                    "step": step,
                    "status": "INFO",
                    "outcome": "No matching tool required."
                })

        report["finished"] = datetime.now().isoformat(timespec="seconds")

        return report


############################################################

if __name__ == "__main__":

    registry = ToolRegistry()

    registry.register(
        "Code Executor",
        DummyTool("Code Executor")
    )

    registry.register(
        "Experiment Engine",
        DummyTool("Experiment Engine")
    )

    registry.register(
        "Android Agent",
        DummyTool("Android Agent")
    )

    planner = TaskPlanner(registry)

    plan = planner.create_plan(
        "Run a Python experiment then open GitHub"
    )

    executor = TaskExecutor(registry)

    report = executor.execute(plan)

    print()
    print("=" * 60)
    print("EXECUTION REPORT")
    print("=" * 60)
    print()

    print("Goal:")
    print(report["goal"])
    print()

    for i, result in enumerate(report["results"], 1):

        print(f"Step {i}")
        print(" Status :", result["status"])
        print(" Action :", result["step"])
        print(" Result :", result["outcome"])
        print()

    print("Started :", report["started"])
    print("Finished:", report["finished"])
