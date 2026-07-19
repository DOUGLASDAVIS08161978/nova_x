#!/usr/bin/env python3
"""
===========================================================
NOVA-X Knowledge Query Engine v1.0
===========================================================

Provides search and retrieval over the Knowledge Graph.

Features:
- Find entities
- Search relationships
- Inspect connected concepts

===========================================================
"""

from memory.knowledge_graph import KnowledgeGraph


class KnowledgeQueryEngine:

    def __init__(self):

        self.kg = KnowledgeGraph()


    def find_entity(self, name):

        entities = self.kg.graph["entities"]

        if name in entities:

            return entities[name]

        return None


    def search_entities(self, keyword):

        results = []

        keyword = keyword.lower()

        for name, data in self.kg.graph["entities"].items():

            if keyword in name.lower():

                results.append({

                    "name": name,

                    "data": data

                })

        return results


    def relationships_for(self, entity):

        results = []

        for relation in self.kg.graph["relationships"]:

            if (
                relation["source"] == entity
                or
                relation["target"] == entity
            ):

                results.append(relation)

        return results


    def stats(self):

        return self.kg.summary()


if __name__ == "__main__":

    engine = KnowledgeQueryEngine()


    print()

    print("NOVA-X Knowledge Query Engine")

    print("============================")

    print()

    print("Search: bicycle")

    print("----------------")

    print(
        engine.search_entities("bicycle")
    )

    print()

    print("Graph Stats")

    print("-----------")

    print(
        engine.stats()
    )

