#!/usr/bin/env python3
"""
===========================================================
                 NOVA-X Reasoning Manager v2.2
===========================================================

Identity-aware reasoning gateway.

Features
--------
- Identity Context
- Conversation Memory
- Groq Engine
- Automatic conversation persistence
- Engine status/history

===========================================================
"""

from datetime import datetime

from plugins.groq_engine import GroqEngine
from cognition.identity_context import IdentityContext
from memory.conversation_memory import ConversationMemory


class ReasoningManager:

    def __init__(self):
        self.engines = {}
        self.history = []

        self.identity = IdentityContext()
        self.conversation = ConversationMemory()

        self.load_engines()

    def load_engines(self):
        try:
            self.engines["groq"] = GroqEngine()
            print("[ReasoningManager] Groq engine loaded.")
        except Exception as e:
            print("[ReasoningManager] Engine error:", e)

    def reason(self, prompt):

        identity_context = self.identity.build_context()

        conversation_context = self.conversation.context(limit=8)

        full_prompt = f"""{identity_context}

Recent Conversation
===================

{conversation_context}

Current User Request
====================

{prompt}

Respond naturally as NOVA-X.

Use the recent conversation whenever it is relevant.
If there is no relevant conversation history, simply answer normally.
"""

        engine = self.engines.get("groq")

        if not engine:
            return {
                "success": False,
                "response": "No reasoning engine available."
            }

        try:

            # Remember the user's message first
            self.conversation.remember("Douglas", prompt)

            # Ask Groq
            response = engine.ask(full_prompt)

            # Remember NOVA-X's reply
            self.conversation.remember("NOVA-X", response)

            # Keep runtime history
            self.history.append({
                "timestamp": str(datetime.now()),
                "prompt": prompt,
                "response": response,
                "engine": "groq"
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
        """
        Returns loaded reasoning engines.
        """
        return list(self.engines.keys())

    def status(self):
        return {
            "engines": list(self.engines.keys()),
            "history": len(self.history),
            "conversation_messages": self.conversation.stats()["messages"]
        }


if __name__ == "__main__":

    rm = ReasoningManager()

    result = rm.reason("Introduce yourself.")

    print()
    print(result)
