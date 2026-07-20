#!/usr/bin/env python3
"""
===========================================================
NOVA-X Android Agent v1.0
===========================================================

Provides a controlled interface between NOVA-X and Android.

Author:
Douglas Davis & OpenAI

===========================================================
"""

import subprocess


class AndroidAgent:

    def __init__(self):
        self.version = "1.0"

    def _run(self, command):

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {

                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode

            }

        except Exception as e:

            return {

                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1

            }

    ########################################################
    # Browser
    ########################################################

    def open_url(self, url):

        return self._run(

            f'am start -a android.intent.action.VIEW -d "{url}"'

        )

    ########################################################
    # Share text
    ########################################################

    def share_text(self, text):

        return self._run(

            f'am start -a android.intent.action.SEND '
            f'-t text/plain --es android.intent.extra.TEXT "{text}"'

        )

    ########################################################
    # Open local file
    ########################################################

    def open_file(self, filename):

        return self._run(

            f'am start -a android.intent.action.VIEW '
            f'-d "file://{filename}"'

        )

    ########################################################
    # Approved shell commands
    ########################################################

    def run_command(self, command):

        allowed = [

            "pwd",
            "ls",
            "whoami",
            "python3 --version",
            "git status"

        ]

        if command not in allowed:

            return {

                "success": False,
                "stdout": "",
                "stderr": "Command not approved.",
                "returncode": -1

            }

        return self._run(command)


############################################################

if __name__ == "__main__":

    agent = AndroidAgent()

    print("=" * 55)
    print("ANDROID AGENT")
    print("=" * 55)

    print("\nOpening GitHub...")

    result = agent.open_url(

        "https://github.com"

    )

    print(result)

    print("\nRunning approved command...\n")

    print(

        agent.run_command(

            "pwd"

        )

    )
