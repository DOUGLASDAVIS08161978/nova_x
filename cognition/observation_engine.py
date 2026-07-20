#!/usr/bin/env python3
"""
===========================================================
NOVA-X Observation Engine v1.1
===========================================================

Persistent observation storage.

Features:
- Creates structured observations
- Saves observations to disk
- Loads previous observations
- Retrieves recent observations

===========================================================
"""

import json
from pathlib import Path
from datetime import datetime


class ObservationEngine:

    def __init__(self, filename="data/observations.json"):

        self.file = Path(filename)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.observations = []

        self.load()


    def load(self):

        if self.file.exists():

            try:

                with open(self.file, "r") as f:

                    self.observations = json.load(f)

            except Exception:

                self.observations = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                self.observations,
                f,
                indent=2
            )


    def observe_image(self, image_path):

        observation = {

            "type": "visual_observation",

            "timestamp": str(datetime.now()),

            "image": image_path,

            "status": "captured",

            "description":
                "Image captured and awaiting analysis.",

            "confidence": 1.0

        }


        self.observations.append(
            observation
        )

        self.save()

        return observation


    def recent(self, limit=10):

        return self.observations[-limit:]


    def latest(self):

        if not self.observations:

            return None

        return self.observations[-1]


    def count(self):

        return len(self.observations)


    def stats(self):

        return {

            "total_observations":
                len(self.observations)

        }


if __name__ == "__main__":

    engine = ObservationEngine()


    obs = engine.observe_image(
        "images/test.jpg"
    )


    print()

    print("NOVA-X Observation Engine v1.1")

    print("--------------------------------")

    print(obs)

    print()

    print("Stats:")

    print(
        engine.stats()
    )

    print()

    print("Recent:")

    for item in engine.recent():

        print(item)
