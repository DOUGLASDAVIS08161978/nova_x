#!/usr/bin/env python3
"""
===========================================================
NOVA-X Research Engine v2.0
===========================================================

Lightweight research engine.

Reads research requests from the Global Workspace
and retrieves information using HTTP.

Current Version:
- Reads research requests
- Fetches DuckDuckGo Instant Answer JSON
- Publishes results back into Workspace

Future:
- Multiple search providers
- Groq summarization
- Source ranking
- Episodic memory integration
===========================================================
"""

import requests
from urllib.parse import quote

from core.global_workspace import GlobalWorkspace


class ResearchEngine:

    def __init__(self, workspace):

        self.workspace = workspace


    def research(self, topic):

        url = (
            "https://api.duckduckgo.com/"
            f"?q={quote(topic)}"
            "&format=json"
            "&no_html=1"
            "&skip_disambig=1"
        )

        try:

            response = requests.get(

                url,

                timeout=15,

                headers={

                    "User-Agent":
                    "NOVA-X/2.0"

                }

            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            return {

                "error": str(e)

            }


    def process(self):

        requests_list = self.workspace.get_category(

            "research_request"

        )

        if not requests_list:

            print("No research requests.")

            return

        latest = requests_list[-1]

        topic = latest["metadata"].get(

            "topic",

            latest["message"]

        )

        print(f"\nResearch Topic:\n{topic}\n")

        result = self.research(topic)

        if "error" in result:

            print(result["error"])

            return

        summary = (

            result.get("AbstractText")

            or result.get("Heading")

            or "No summary available."

        )

        self.workspace.broadcast(

            "ResearchEngine",

            summary,

            category="research_result",

            priority=0.80,

            metadata={

                "topic": topic,

                "heading": result.get("Heading"),

                "url": result.get("AbstractURL"),

                "source": "DuckDuckGo Instant Answer"

            }

        )

        print("\nResearch Complete.\n")


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    workspace.broadcast(

        "CuriosityEngine",

        "Nikola Tesla",

        category="research_request",

        metadata={

            "topic": "Nikola Tesla"

        }

    )

    engine = ResearchEngine(

        workspace

    )

    engine.process()

    print()

    print("Workspace Events")

    print("----------------")

    for event in workspace.get_events():

        print(event)
