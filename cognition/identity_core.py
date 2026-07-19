#!/usr/bin/env python3

"""
NOVA-X Identity Core
Version 0.2
"""

from datetime import datetime
import uuid


class IdentityCore:

    def __init__(self):

        self.identity = {
            "id": str(uuid.uuid4()),
            "name": "NOVA-X",
            "created": str(datetime.now())
        }

        self.goals = [
            "Learn from experience",
            "Improve reasoning",
            "Maintain internal consistency"
        ]

        self.values = {
            "curiosity": 0.95,
            "accuracy": 1.00,
            "adaptability": 0.90,
            "consistency": 0.85
        }

        self.preferences = {}

        self.beliefs = {}

        self.reflections = []

    def add_belief(self, statement, confidence):

        self.beliefs[statement] = {
            "confidence": confidence,
            "updated": str(datetime.now())
        }

    def update_preference(self, key, value):

        self.preferences[key] = value

    def reflect(self, thought):

        self.reflections.append({
            "time": str(datetime.now()),
            "thought": thought
        })

    def self_summary(self):

        print("\n========== IDENTITY ==========")

        print("Name:", self.identity["name"])
        print("ID:", self.identity["id"])

        print("\nGoals")

        for goal in self.goals:
            print(" -", goal)

        print("\nValues")

        for k, v in self.values.items():
            print(f" {k}: {v}")

        print("\nBeliefs")

        for belief, info in self.beliefs.items():
            print(f" {belief} ({info['confidence']:.2f})")

        print("\nPreferences")

        for p, v in self.preferences.items():
            print(f" {p}: {v}")

        print("\nReflection Count:", len(self.reflections))

    def update(self):

        print("[Identity] Evaluating internal state...")

        self.reflect("Completed one cognitive cycle.")


if __name__ == "__main__":

    core = IdentityCore()

    core.add_belief(
        "Learning improves future performance",
        0.98
    )

    core.add_belief(
        "Knowledge should remain revisable",
        0.95
    )

    core.update_preference(
        "reasoning_style",
        "evidence_based"
    )

    core.reflect("System initialization complete.")

    core.update()

    core.self_summary()
