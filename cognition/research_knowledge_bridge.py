#!/usr/bin/env python3
"""
===========================================================
NOVA-X Research Knowledge Bridge v1.1
===========================================================

Converts research summaries into Knowledge Graph entries.

Improvements:
- Basic entity normalization
- Multi-word name detection
- Cleaner graph entries
- Preserves KnowledgeGraph compatibility

===========================================================
"""

import re

from memory.knowledge_graph import KnowledgeGraph


class ResearchKnowledgeBridge:

    def __init__(self):

        self.kg = KnowledgeGraph()


    def extract_entities(self, text):

        entities = set()


        # Capture multi-word proper names
        patterns = re.findall(
            r"\b[A-Z][a-zA-Z0-9\-]+(?:\s+[A-Z][a-zA-Z0-9\-]+)+\b",
            text
        )


        for item in patterns:

            if len(item) > 3:

                entities.add(item.strip())


        # Capture single important capitalized terms
        singles = re.findall(
            r"\b[A-Z][a-zA-Z0-9\-]{3,}\b",
            text
        )


        for item in singles:

            if item not in {
                "The",
                "This",
                "While",
                "With"
            }:

                entities.add(item)


        return sorted(entities)


    def import_research(self, title, summary):

        topic = f"Research:{title}"


        self.kg.add_entity(
            topic,
            "research"
        )


        entities = self.extract_entities(
            summary
        )


        for entity in entities:

            self.kg.add_entity(
                entity,
                "concept"
            )


            self.kg.add_relationship(

                topic,

                "mentions",

                entity

            )


        return {

            "topic": topic,

            "entities_imported":
                len(entities)

        }


if __name__ == "__main__":


    bridge = ResearchKnowledgeBridge()


    summary = """
Nikola Tesla developed alternating current
technology. Tesla created the Tesla Coil and
worked on the Wardenclyffe Tower project for
wireless power transmission.
"""


    result = bridge.import_research(

        "Nikola Tesla",

        summary

    )


    print()

    print("Research Knowledge Bridge v1.1")

    print("------------------------------")

    print(result)

    print()

    print("Knowledge Graph")

    print("----------------")

    print(
        bridge.kg.summary()
    )
