#!/usr/bin/env python3
"""
===========================================================
NOVA-X Knowledge Context Builder v1.0
===========================================================

Builds a textual knowledge context for the Reasoning Manager.

Features
--------
- Searches the Knowledge Graph
- Finds matching entities
- Lists related relationships
- Produces prompt-ready context

===========================================================
"""

from cognition.knowledge_query_engine import KnowledgeQueryEngine


class KnowledgeContext:

    def __init__(self):

        self.query = KnowledgeQueryEngine()


    def build_context(self, prompt):

        words = []

        for word in prompt.lower().split():

            word = word.strip(".,!?()[]{}\"'")

            if len(word) > 2:

                words.append(word)


        entities = []

        relationships = []


        for word in words:

            matches = self.query.search_entities(word)

            for match in matches:

                if match not in entities:

                    entities.append(match)

                    rels = self.query.relationships_for(
                        match["name"]
                    )

                    relationships.extend(rels)


        lines = []

        lines.append("Knowledge Context")

        lines.append("=================")

        if not entities:

            lines.append("No relevant knowledge found.")

            return "\n".join(lines)


        lines.append("Entities:")

        for entity in entities:

            data = entity["data"]

            lines.append(
                f"- {entity['name']} "
                f"({data['type']}, "
                f"mentions={data['mentions']})"
            )


        if relationships:

            lines.append("")

            lines.append("Relationships:")

            for rel in relationships:

                lines.append(

                    f"- {rel['source']} "

                    f"{rel['relation']} "

                    f"{rel['target']}"

                )


        return "\n".join(lines)


if __name__ == "__main__":

    kc = KnowledgeContext()

    prompt = "Tell me about the electric bicycle."

    print()

    print(kc.build_context(prompt))

