"""
═══════════════════════════════════════════════════════════════════════
NOVA-X RESEARCH ENGINE
═══════════════════════════════════════════════════════════════════════

Consumes research requests from the workspace.

Author:
Douglas Davis & OpenAI
"""

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "daemon")
)

from runtime import NovaRuntime
from mission_manager import Mission


class ResearchEngine:

    def __init__(self, runtime):

        self.runtime = runtime

    def cycle(self):

        if not self.runtime.workspace.has_work():

            print("[Research] No work available.")
            return

        task = self.runtime.workspace.next_task()

        if task["type"] != "research_request":

            print(
                f"[Research] Ignoring task: {task['type']}"
            )
            return

        topic = task["payload"].get(
            "mission",
            "Unknown Topic"
        )

        print()

        print("=" * 55)
        print("RESEARCH ENGINE")
        print("=" * 55)

        print()

        print(f"Research Topic : {topic}")

        result = {
            "topic": topic,
            "status": "completed",
            "summary":
                f"Research cycle completed for '{topic}'."
        }

        self.runtime.workspace.submit(
            "Research",
            "knowledge_update",
            result
        )

        self.runtime.heartbeat.research()

        print()

        print("[Research] Cycle complete.")


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    runtime = NovaRuntime()

    runtime.missions.add(
        Mission(
            "Improve Battery Technology",
            "HIGH"
        )
    )

    runtime.workspace.submit(
        "Curiosity",
        "research_request",
        {
            "mission":
                "Improve Battery Technology"
        }
    )

    engine = ResearchEngine(runtime)

    engine.cycle()

    print()

    runtime.workspace.status()
