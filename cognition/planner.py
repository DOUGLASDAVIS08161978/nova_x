#!/usr/bin/env python3
"""
===========================================================
NOVA-X Planner v1.0
===========================================================

Converts decisions into executable task plans.

Current Capabilities
--------------------
- Plan from Decision Engine actions
- Prioritized task lists
- Workspace publication

Future
------
- Dynamic planning
- Task dependencies
- Replanning
- Multi-step execution
===========================================================
"""

from core.global_workspace import GlobalWorkspace


class Planner:

    def __init__(self, workspace):

        self.workspace = workspace


    def create_plan(self, decision):

        action = decision.get("action", "")

        if action == "investigate_contradiction":

            tasks = [

                "Retrieve contradiction",

                "Collect related workspace events",

                "Ask Groq for analysis",

                "Generate summary",

                "Store result in memory"

            ]

        elif action == "focus_high_priority":

            tasks = [

                "Retrieve urgent event",

                "Analyze importance",

                "Recommend response"

            ]

        elif action == "advance_goal":

            tasks = [

                "Retrieve goal",

                "Determine next milestone",

                "Recommend next action"

            ]

        else:

            tasks = [

                "Review workspace",

                "Learn from recent events"

            ]

        return tasks


    def publish_plan(self, tasks):

        for i, task in enumerate(tasks, start=1):

            self.workspace.broadcast(

                "Planner",

                task,

                category="plan",

                priority=0.80,

                metadata={

                    "step": i,

                    "total_steps": len(tasks)

                }

            )


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    planner = Planner(workspace)

    decision = {

        "action": "investigate_contradiction"

    }

    plan = planner.create_plan(decision)

    planner.publish_plan(plan)

    print()

    print("Generated Plan")

    print("----------------")

    for step, task in enumerate(plan, start=1):

        print(f"{step}. {task}")
