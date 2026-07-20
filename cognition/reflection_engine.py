"""
═══════════════════════════════════════════════════════════════════════
NOVA-X REFLECTION ENGINE
═══════════════════════════════════════════════════════════════════════

Reflects on newly acquired knowledge.

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


class ReflectionEngine:

    def __init__(self, runtime):

        self.runtime = runtime

    def cycle(self):

        if not self.runtime.workspace.has_work():

            print("[Reflection] No work.")
            return

        task = self.runtime.workspace.next_task()

        if task["type"] != "reflection_request":

            print(
                f"[Reflection] Ignoring {task['type']}"
            )
            return

        knowledge = task["payload"]

        print()
        print("=" * 55)
        print("REFLECTION ENGINE")
        print("=" * 55)
        print()

        print(
            f"Topic : {knowledge.get('topic')}"
        )

        summary = knowledge.get(
            "summary",
            ""
        )

        insight = (
            f"Reflection completed for "
            f"{knowledge.get('topic')}."
        )

        print(f"Summary : {summary}")
        print(f"Insight : {insight}")

        self.runtime.heartbeat.reflection()

        self.runtime.workspace.submit(

            "Reflection",

            "journal_entry",

            {
                "topic": knowledge.get("topic"),
                "summary": summary,
                "insight": insight
            }

        )

        print()
        print("[Reflection] Cycle complete.")


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    runtime = NovaRuntime()

    runtime.workspace.submit(

        "Knowledge",

        "reflection_request",

        {
            "topic":"Improve Battery Technology",
            "summary":"Research completed successfully."
        }

    )

    engine = ReflectionEngine(runtime)

    engine.cycle()

    print()

    runtime.workspace.status()
