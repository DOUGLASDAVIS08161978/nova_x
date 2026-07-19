#!/usr/bin/env python3
"""
===========================================================
NOVA-X Vision Knowledge Bridge v1.0
===========================================================

Transfers Vision Analyzer results into the Knowledge Graph.

Current Features
----------------
- Stores detected objects as entities
- Links observations to objects
- Ready for future vision models

===========================================================
"""

from datetime import datetime

from memory.knowledge_graph import KnowledgeGraph


class VisionKnowledgeBridge:

    def __init__(self):

        self.kg = KnowledgeGraph()

        self.imported = 0


    def import_analysis(self, analysis):

        image = analysis.get(
            "image",
            "unknown_image"
        )

        observation = (
            f"Observation:{image}"
        )

        self.kg.add_entity(
            observation,
            "observation"
        )


        objects = analysis.get(
            "objects",
            []
        )


        for obj in objects:

            self.kg.add_entity(
                obj,
                "object"
            )

            self.kg.add_relationship(

                observation,

                "contains",

                obj

            )


        self.imported += 1

        return {

            "observation": observation,

            "objects_imported": len(objects),

            "timestamp": str(datetime.now())

        }


    def status(self):

        return {

            "imports": self.imported,

            "graph": self.kg.summary()

        }


if __name__ == "__main__":

    bridge = VisionKnowledgeBridge()


    sample_analysis = {

        "image": "images/test.jpg",

        "description":
            "Yellow fat tire electric bicycle",

        "objects": [

            "electric bicycle",

            "wheel",

            "rear rack"

        ],

        "confidence": 0.96

    }


    result = bridge.import_analysis(
        sample_analysis
    )


    print()

    print("Vision Knowledge Bridge")

    print("-----------------------")

    print(result)

    print()

    print("Knowledge Graph")

    print("----------------")

    print(
        bridge.status()
    )

