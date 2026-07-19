#!/usr/bin/env python3
"""
===========================================================
NOVA-X Decision Engine v1.0
===========================================================

Chooses the next action for NOVA-X based on the
current Global Workspace.

Decision Priority

1. Contradictions
2. High Priority Events
3. Active Goals
4. Idle Learning

===========================================================
"""

from core.global_workspace import GlobalWorkspace


class DecisionEngine:

    def __init__(self, workspace):

        self.workspace = workspace


    def decide(self):

        events = self.workspace.get_events()

        # Highest priority:
        # investigate contradictions

        contradictions = [

            e for e in events

            if e["category"] == "contradiction"

        ]

        if contradictions:

            return {

                "action": "investigate_contradiction",

                "reason":
                    f"{len(contradictions)} contradiction(s) detected."

            }


        # High priority items

        urgent = self.workspace.get_high_priority(0.85)

        if urgent:

            return {

                "action": "focus_high_priority",

                "reason":
                    f"{len(urgent)} urgent event(s)."

            }


        # Active goals

        goals = self.workspace.get_category("goal")

        if goals:

            return {

                "action": "advance_goal",

                "reason":
                    goals[0]["message"]

            }


        return {

            "action": "idle_learning",

            "reason":
                "No urgent cognitive work."

        }


    def execute(self):

        decision = self.decide()

        self.workspace.broadcast(

            "DecisionEngine",

            decision["reason"],

            category="decision",

            priority=0.95,

            metadata=decision

        )

        return decision


if __name__ == "__main__":

    gw = GlobalWorkspace()

    gw.broadcast(

        "Planner",

        "Improve memory retrieval.",

        category="goal",

        priority=0.70

    )

    gw.broadcast(

        "ConsistencyChecker",

        "Rise vs Fall detected.",

        category="contradiction",

        priority=0.99

    )

    engine = DecisionEngine(gw)

    decision = engine.execute()

    print()

    print("Decision")

    print("--------")

    print(decision)

    print()

    print("Workspace")

    print("---------")

    for event in gw.get_events():

        print(event)
