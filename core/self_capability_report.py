#!/usr/bin/env python3
"""
============================================================
NOVA-X Self Capability Reporter v1.0
============================================================

Reads the Capability Registry and produces a dynamic
self-description.

Douglas Davis & OpenAI
============================================================
"""

import json
from pathlib import Path

REGISTRY = Path.home() / "nova_x" / "capability_registry.json"


class SelfCapabilityReporter:

    def __init__(self):

        self.capabilities = {}

    def load(self):

        if REGISTRY.exists():
            self.capabilities = json.loads(
                REGISTRY.read_text()
            )

    def enabled(self):

        return {
            name: info
            for name, info in self.capabilities.items()
            if info.get("enabled", False)
        }

    def report(self):

        enabled = self.enabled()

        print()
        print("=" * 60)
        print("NOVA-X CURRENT CAPABILITIES")
        print("=" * 60)
        print()

        for name in sorted(enabled):

            info = enabled[name]

            print(f"✓ {name}")
            print(f"    Provider    : {info['provider']}")
            print(f"    Description : {info['description']}")
            print()

        print("=" * 60)
        print(f"Enabled Capabilities : {len(enabled)}")
        print("=" * 60)

    def self_description(self):

        enabled = self.enabled()

        text = []

        text.append(
            "Based on my current architecture, I presently have access to:"
        )

        for name in sorted(enabled):

            text.append(f"- {name}: {enabled[name]['description']}")

        text.append("")
        text.append(
            "My capabilities reflect the modules currently enabled in my local NOVA-X system."
        )

        return "\n".join(text)


if __name__ == "__main__":

    reporter = SelfCapabilityReporter()

    reporter.load()

    reporter.report()

    print()
    print("SELF DESCRIPTION")
    print("----------------")
    print()

    print(reporter.self_description())

