#!/usr/bin/env python3
"""
===========================================================
NOVA-X Reasoning Manager v2.0
===========================================================

Central reasoning coordinator.

Responsibilities:
- Manage reasoning engines
- Route requests
- Track reasoning history
- Provide structured responses
- Support future AI backends

===========================================================
"""

from datetime import datetime
import traceback


class ReasoningManager:

    def __init__(self):

        self.engines = {}

        self.history = []

        self.load_engines()


    # -----------------------------------------------------

    def load_engines(self):

        try:

            from plugins.groq_engine import GroqEngine

            self.engines["groq"] = GroqEngine()

            print(
                "[ReasoningManager] Groq engine loaded."
            )

        except Exception as error:

            print(
                "[ReasoningManager] Groq failed:",
                error
            )


    # -----------------------------------------------------

    def available_engines(self):

        return list(self.engines.keys())


    # -----------------------------------------------------

    def status(self):

        return {

            "engines":
                self.available_engines(),

            "history_entries":
                len(self.history),

            "timestamp":
                str(datetime.now())

        }


    # -----------------------------------------------------

    def reason(
        self,
        prompt,
        engine="groq"
    ):

        request = {

            "time":
                str(datetime.now()),

            "engine":
                engine,

            "prompt":
                prompt
        }


        try:

            if engine not in self.engines:

                raise ValueError(
                    f"Engine unavailable: {engine}"
                )


            selected = self.engines[engine]


            response = selected.ask(prompt)


            result = {

                "success":
                    True,

                "engine":
                    engine,

                "response":
                    response,

                "time":
                    str(datetime.now())

            }


            self.history.append(
                {
                    "request": request,
                    "result": result
                }
            )


            return result


        except Exception as error:


            result = {

                "success":
                    False,

                "error":
                    str(error),

                "trace":
                    traceback.format_exc()

            }


            self.history.append(
                {
                    "request": request,
                    "result": result
                }
            )


            return result


    # -----------------------------------------------------

    def show_history(self):

        print("\n===== Reasoning History =====")

        for item in self.history:

            print(
                item["request"]["prompt"]
            )

            print(
                "Success:",
                item["result"]["success"]
            )

            print()



# =========================================================
# Test
# =========================================================

if __name__ == "__main__":


    manager = ReasoningManager()


    print("\nAvailable Engines:")

    print(
        manager.available_engines()
    )


    print("\nSystem Status:")

    print(
        manager.status()
    )


    print(
        "\nTesting Reasoning...\n"
    )


    result = manager.reason(
        "Explain why modular AI systems are easier to improve."
    )


    if result["success"]:

        print(
            result["response"]
        )

    else:

        print(
            "ERROR:",
            result["error"]
        )


    manager.show_history()
