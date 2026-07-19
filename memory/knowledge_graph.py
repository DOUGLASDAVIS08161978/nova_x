#!/usr/bin/env python3
"""
===========================================================
NOVA-X Knowledge Graph v1.0
===========================================================

Stores entities and relationships discovered during research.

Current Version
---------------
- Entity storage
- Simple relationships
- Persistent JSON database

Future
------
- Graph search
- Confidence weighting
- Semantic clustering
- Belief updates
===========================================================
"""

import json
from pathlib import Path


class KnowledgeGraph:

    def __init__(self,
                 filename="data/knowledge_graph.json"):

        self.file = Path(filename)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.graph = {

            "entities": {},

            "relationships": []

        }

        self.load()


    def load(self):

        if self.file.exists():

            try:

                with open(self.file, "r") as f:

                    self.graph = json.load(f)

            except Exception:

                pass


    def save(self):

        with open(self.file, "w") as f:

            json.dump(

                self.graph,

                f,

                indent=2

            )


    def add_entity(

        self,

        name,

        entity_type="concept"

    ):

        if name not in self.graph["entities"]:

            self.graph["entities"][name] = {

                "type": entity_type,

                "mentions": 1

            }

        else:

            self.graph["entities"][name]["mentions"] += 1

        self.save()


    def add_relationship(

        self,

        source,

        relation,

        target

    ):

        self.graph["relationships"].append({

            "source": source,

            "relation": relation,

            "target": target

        })

        self.save()


    def summary(self):

        return {

            "entities":

                len(self.graph["entities"]),

            "relationships":

                len(self.graph["relationships"])

        }


if __name__ == "__main__":

    kg = KnowledgeGraph()

    kg.add_entity(

        "Nikola Tesla",

        "person"

    )

    kg.add_entity(

        "Alternating Current",

        "technology"

    )

    kg.add_relationship(

        "Nikola Tesla",

        "developed",

        "Alternating Current"

    )

    print()

    print("Knowledge Graph Summary")

    print("-----------------------")

    print(

        kg.summary()

    )

    print()

    print(kg.graph)
