#!/usr/bin/env python3
"""
============================================================
NOVA-X Capability Router
Routes capability-related questions to the dynamic
SelfCapabilityReporter.
============================================================
"""

from core.self_capability_report import SelfCapabilityReporter


CAPABILITY_KEYWORDS = [
    "capabilities",
    "capability",
    "what can you do",
    "what are your abilities",
    "abilities",
    "features",
    "functions",
    "what do you do",
    "tell me about yourself",
]


def is_capability_question(text):

    text = text.lower()

    return any(keyword in text for keyword in CAPABILITY_KEYWORDS)


def capability_response():

    reporter = SelfCapabilityReporter()

    reporter.load()

    return reporter.self_description()

