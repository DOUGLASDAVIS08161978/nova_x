#!/usr/bin/env python3
"""
===========================================================
NOVA-X Reasoning Manager v2.0
===========================================================

Identity-aware reasoning gateway.

Connects:
- Identity Context
- Groq Engine

===========================================================
"""

from datetime import datetime

from plugins.groq_engine import GroqEngine
from cognition.identity_context import IdentityContext


class ReasoningManager:


    def __init__(self):

        self.engines = {}

        self.history = []

        self.identity = IdentityContext()

        self.load_engines()


    def load_engines(self):

        try:

            self.engines["groq"] = GroqEngine()

            print(
                "[ReasoningManager] Groq engine loaded."
            )

        except Exception as e:

            print(
                "[ReasoningManager] Engine error:",
                e
            )


    def reason(self, prompt):

        context = self.identity.build_context()

        full_prompt = f"""
{context}

User request:

{prompt}

Provide a helpful, accurate response.
"""


        engine = self.engines.get("groq")


        if not engine:

            return {

                "success": False,

                "response":
                    "No reasoning engine available."

            }


        try:

            response = engine.generate(
                full_prompt
            )


            record = {

                "timestamp":
                    str(datetime.now()),

                "prompt":
                    prompt,

                "response":
                    response,

                "engine":
                    "groq"

            }


            self.history.append(record)


            return {

                "success": True,

                "response": response

            }


        except Exception as e:

            return {

                "success": False,

                "response": str(e)

            }


    def status(self):

        return {

            "engines":
                list(self.engines.keys()),

            "history":
                len(self.history)

        }


if __name__ == "__main__":

    rm = ReasoningManager()

    result = rm.reason(
        "Introduce yourself."
    )

    print()

    print(result)

