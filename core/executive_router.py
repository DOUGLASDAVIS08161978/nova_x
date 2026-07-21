#!/usr/bin/env python3
"""
============================================================
NOVA-X Executive Router v1.0
============================================================

Routes user requests to the correct subsystem.

Current Routes

- Capability Reporter
- Pull Request Manager
- Goal Planner (placeholder)
- Repository Intelligence (placeholder)
- Reasoning Manager (fallback)

============================================================
"""

import re

from core.capability_router import (
    is_capability_question,
    capability_response,
)

from core.pull_request_manager import PullRequestManager


class ExecutiveRouter:

    def __init__(self, reasoning_manager):

        self.reasoning = reasoning_manager

    def route(self, prompt):

        text = prompt.lower().strip()

        # ----------------------------------------------------
        # Capability Questions
        # ----------------------------------------------------

        if is_capability_question(text):

            return capability_response()

        # ----------------------------------------------------
        # Pull Requests
        # ----------------------------------------------------

        if (
            "pull request" in text
            or "create pr" in text
            or "make a pr" in text
        ):

            title = prompt

            title = re.sub(
                r"(?i)create|make|open|please|a|pull request|pr|to",
                "",
                title,
            )

            title = " ".join(title.split()).strip()

            if not title:
                title = "NOVA-X Improvement"

            manager = PullRequestManager()

            manager.create_pull_request(
                title=title,
                body="Autonomously proposed by NOVA-X."
            )

            return "Pull Request workflow complete."

        # ----------------------------------------------------
        # Future Routes
        # ----------------------------------------------------

        if "repository" in text:
            return (
                "Repository Intelligence routing "
                "will be connected in v2."
            )

        if "plan" in text:
            return (
                "Goal Planner routing "
                "will be connected in v2."
            )

        # ----------------------------------------------------
        # Default
        # ----------------------------------------------------

        result = self.reasoning.reason(prompt)

        if isinstance(result, str):
            return result

        if isinstance(result, dict):

            for key in (
                "response",
                "text",
                "message",
            ):
                if key in result:
                    return result[key]

        return str(result)
