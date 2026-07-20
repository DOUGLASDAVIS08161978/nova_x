#!/usr/bin/env python3
"""
===========================================================
NOVA-X Code Executor
===========================================================

Executes Python code in an isolated subprocess.

Returns:
    success
    stdout
    stderr
    returncode
    execution_time

===========================================================
"""

import os
import sys
import time
import tempfile
import subprocess


class CodeExecutor:

    def __init__(self, timeout=30):
        self.timeout = timeout

    def execute_python(self, code):

        start = time.time()

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as f:

            f.write(code)
            filename = f.name

        try:

            result = subprocess.run(
                [sys.executable, filename],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            elapsed = time.time() - start

            return {

                "success": result.returncode == 0,

                "stdout": result.stdout,

                "stderr": result.stderr,

                "returncode": result.returncode,

                "execution_time": round(elapsed, 3)

            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "stdout": "",

                "stderr": "Execution timed out.",

                "returncode": -1,

                "execution_time": self.timeout

            }

        finally:

            try:
                os.remove(filename)
            except Exception:
                pass


if __name__ == "__main__":

    executor = CodeExecutor()

    code = '''
print("Hello from NOVA-X!")
print(2 + 2)
'''

    result = executor.execute_python(code)

    print("=" * 55)
    print("CODE EXECUTOR TEST")
    print("=" * 55)

    for key, value in result.items():
        print(f"{key}:")
        print(value)
        print()
