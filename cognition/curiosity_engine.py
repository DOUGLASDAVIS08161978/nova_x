#!/usr/bin/env python3
"""
===========================================================
NOVA-X Curiosity Engine v1.0
===========================================================

Generates research topics based on:
- Active goals
- Workspace activity
- Random exploration

This module DOES NOT perform research.
It decides what should be researched next.
===========================================================
"""

import random

from core.global_workspace import GlobalWorkspace


DEFAULT_TOPICS = [

    "Artificial Intelligence",

    "Memory Systems",

    "Planning Algorithms",

    "Distributed Systems",

    "Knowledge Graphs",

    "Software Architecture",

    "Machine Learning",

    "Robotics",

    "Cybersecurity",

    "Mathematics"

]


class CuriosityEngine:

    def __init__(self, workspace):

        self.workspace = workspace


    def choose_topic(self):

        goals = self.workspace.get_category("goal")

        if goals:

            goal = random.choice(goals)

            return f"Research goal: {goal['message']}"

        return random.choice(DEFAULT_TOPICS)


    def generate(self):

        topic = self.choose_topic()

        self.workspace.broadcast(

            "CuriosityEngine",

            topic,

            category="research_request",

            priority=0.80,

            metadata={

                "topic": topic,

                "origin": "curiosity"

            }

        )

        return topic


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    workspace.broadcast(

        "Planner",

        "Improve memory retrieval",

        category="goal"

    )

    engine = CuriosityEngine(

        workspace

    )

    topic = engine.generate()

    print()

    print("Curiosity Selected")

    print("------------------")

    print(topic)
