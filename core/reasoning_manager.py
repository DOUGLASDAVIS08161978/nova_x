#!/usr/bin/env python3
"""
===========================================================
NOVA-X Reasoning Manager v3.0
===========================================================

Identity-aware, conversation-aware, and knowledge-aware
reasoning gateway.

Features
--------
- Identity Context
- Conversation Memory
- Knowledge Context
- Groq Engine
- Automatic conversation persistence
- Engine status/history

===========================================================
"""

from datetime import datetime

from plugins.groq_engine import GroqEngine
from cognition.identity_context import IdentityContext
from cognition.knowledge_context import KnowledgeContext
from memory.conversation_memory import ConversationMemory


class ReasoningManager:

    def __init__(self):

        self.engines = {}

        self.history = []

        self.identity = IdentityContext()

        self.conversation = ConversationMemory()

        self.knowledge = KnowledgeContext()

        self.load_engines()


    def load_engines(self):

        try:

            self.engines["groq"] = GroqEngine()

            print("[ReasoningManager] Groq engine loaded.")

        except Exception as e:

            print("[ReasoningManager] Engine error:", e)


    def reason(self, prompt):

        identity_context = self.identity.build_context()

        conversation_context = self.conversation.context(
            limit=8
        )

        knowledge_context = self.knowledge.build_context(
            prompt
        )


        full_prompt = f"""
{identity_context}

Recent Conversation
===================

{conversation_context}

Knowledge Context
=================

{knowledge_context}

Current User Request
====================

{prompt}

Instructions
============

Respond naturally as NOVA-X.

Use the identity context when relevant.

Use conversation history when it helps.

Use the knowledge context whenever it contains
relevant information.

If there is no relevant knowledge or conversation,
answer normally.
"""


        engine = self.engines.get("groq")

        if not engine:

            return {
                "success": False,
                "response": "No reasoning engine available."
            }


        try:

            self.conversation.remember(
                "Douglas",
                prompt
            )

            response = engine.ask(
                full_prompt
            )

            self.conversation.remember(
                "NOVA-X",
                response
            )

            self.history.append({

                "timestamp":
                    str(datetime.now()),

                "prompt":
                    prompt,

                "response":
                    response,

                "engine":
                    "groq"

            })

            return {

                "success": True,

                "response": response

            }

        except Exception as e:

            return {

                "success": False,

                "response": str(e)

            }


    def available_engines(self):

        return list(
            self.engines.keys()
        )


    def status(self):

        return {

            "engines":
                list(self.engines.keys()),

            "history":
                len(self.history),

            "conversation_messages":
                self.conversation.stats()["messages"]

        }


if __name__ == "__main__":

    rm = ReasoningManager()

    print()

    result = rm.reason(

        "What do you know about the electric bicycle?"

    )

    print(result)
