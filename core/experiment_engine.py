#!/usr/bin/env python3
"""
===========================================================
NOVA-X Experiment Engine v1.0
===========================================================

Runs controlled Python experiments using the Code Executor.

Author:
Douglas Davis & OpenAI

===========================================================
"""

from code_executor import CodeExecutor


class ExperimentEngine:

    def __init__(self):
        self.executor = CodeExecutor()

    def run_experiment(self, title, code):

        print("\n" + "=" * 60)
        print("NOVA-X EXPERIMENT")
        print("=" * 60)
        print("Title :", title)
        print("=" * 60)

        result = self.executor.execute_python(code)

        print("\nExecution Finished\n")

        if result["success"]:
            print("Status : SUCCESS")
        else:
            print("Status : FAILED")

        print("\n----- STDOUT -----")
        print(result["stdout"] or "<empty>")

        print("\n----- STDERR -----")
        print(result["stderr"] or "<empty>")

        print("\nExecution Time:", result["execution_time"], "seconds")

        return result


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    engine = ExperimentEngine()

    sample_code = """
print("Experiment successful!")
total = sum(range(1, 11))
print("Sum =", total)
"""

    engine.run_experiment(
        "Simple Math Experiment",
        sample_code
    )
