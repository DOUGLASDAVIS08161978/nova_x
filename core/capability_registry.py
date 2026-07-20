#!/usr/bin/env python3
"""
============================================================
NOVA-X Capability Registry v1.0
============================================================

Central registry of system capabilities.

This module answers:

- What capabilities exist?
- Which module provides them?
- Is the capability enabled?
- What should other modules call?

Douglas Davis & OpenAI
============================================================
"""

import json
from pathlib import Path

REGISTRY_FILE = Path.home() / "nova_x" / "capability_registry.json"


class CapabilityRegistry:

    def __init__(self):

        self.capabilities = {}

    def register(self, name, provider, description, enabled=True):

        self.capabilities[name] = {
            "provider": provider,
            "description": description,
            "enabled": enabled
        }

    def has(self, name):

        return name in self.capabilities

    def enabled(self, name):

        if name not in self.capabilities:
            return False

        return self.capabilities[name]["enabled"]

    def provider(self, name):

        if name not in self.capabilities:
            return None

        return self.capabilities[name]["provider"]

    def save(self):

        REGISTRY_FILE.write_text(
            json.dumps(
                self.capabilities,
                indent=4
            )
        )

    def load(self):

        if REGISTRY_FILE.exists():

            self.capabilities = json.loads(
                REGISTRY_FILE.read_text()
            )

    def summary(self):

        print()
        print("=" * 60)
        print("NOVA-X CAPABILITY REGISTRY")
        print("=" * 60)
        print()

        for name, info in sorted(self.capabilities.items()):

            state = "ENABLED" if info["enabled"] else "DISABLED"

            print(f"{name}")
            print(f"  Provider    : {info['provider']}")
            print(f"  Status      : {state}")
            print(f"  Description : {info['description']}")
            print()

        print("=" * 60)
        print(f"Total Capabilities: {len(self.capabilities)}")


############################################################

if __name__ == "__main__":

    registry = CapabilityRegistry()

    registry.register(
        "Planning",
        "GoalPlanner",
        "High-level goal planning"
    )

    registry.register(
        "Reasoning",
        "ReasoningManager",
        "Coordinates reasoning engines"
    )

    registry.register(
        "Reflection",
        "ReflectionEngineV2",
        "Post-execution reflection"
    )

    registry.register(
        "Hypothesis Generation",
        "HypothesisEngine",
        "Generates competing explanations"
    )

    registry.register(
        "Repository Intelligence",
        "RepositoryIntelligence",
        "Analyzes repository architecture"
    )

    registry.register(
        "Memory",
        "WorkingMemory",
        "Stores short-term context"
    )

    registry.register(
        "Knowledge Graph",
        "KnowledgeGraph",
        "Persistent structured knowledge"
    )

    registry.register(
        "Vision",
        "VisionAnalyzer",
        "Analyzes images"
    )

    registry.register(
        "Research",
        "ResearchEngine",
        "Searches external knowledge sources"
    )

    registry.save()

    registry.summary()
