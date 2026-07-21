#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
NOVA X SOURCE ANALYZER v1.0
Human-in-the-Loop Engineering Analysis
═══════════════════════════════════════════════════════════════════════

Purpose:
    Analyze Python source code before proposing changes.

This module NEVER edits source code.
"""

from pathlib import Path
from datetime import datetime, UTC
import ast
import json

REPORT_DIR = Path("self_evolution/reports")

WORK_ORDER = REPORT_DIR / "engineering_work_order.json"
OUTPUT = REPORT_DIR / "source_analysis.json"


class FunctionAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):

        end = getattr(node, "end_lineno", node.lineno)

        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "end_line": end,
            "length": end - node.lineno + 1,
            "arguments": len(node.args.args),
            "returns": sum(
                isinstance(n, ast.Return)
                for n in ast.walk(node)
            ),
            "ifs": sum(
                isinstance(n, ast.If)
                for n in ast.walk(node)
            ),
            "loops": sum(
                isinstance(n, (ast.For, ast.While))
                for n in ast.walk(node)
            ),
            "calls": sum(
                isinstance(n, ast.Call)
                for n in ast.walk(node)
            )
        })

        self.generic_visit(node)


class SourceAnalyzer:

    def __init__(self):

        self.report = {
            "generated": datetime.now(UTC).isoformat(),
            "files": [],
            "summary": {}
        }

    def analyze_file(self, path):

        try:

            source = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            visitor = FunctionAnalyzer()

            visitor.visit(tree)

            return {
                "file": str(path),
                "functions": visitor.functions
            }

        except Exception as exc:

            return {
                "file": str(path),
                "error": str(exc)
            }

    def run(self):

        pyfiles = sorted(Path(".").rglob("*.py"))

        total_functions = 0
        long_functions = 0

        for file in pyfiles:

            if "__pycache__" in str(file):
                continue

            result = self.analyze_file(file)

            self.report["files"].append(result)

            for fn in result.get("functions", []):

                total_functions += 1

                if fn["length"] > 75:
                    long_functions += 1

        self.report["summary"] = {

            "python_files":
                len(self.report["files"]),

            "functions":
                total_functions,

            "long_functions":
                long_functions
        }

        return self.report

    def save(self):

        report = self.run()

        with open(
            OUTPUT,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        return report


def main():
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""

    if not WORK_ORDER.exists():

        print("Engineering work order missing.")
        print()
        print("Run:")
        print("python3 self_evolution/work_order_generator.py")
        print()

        return

    analyzer = SourceAnalyzer()

    report = analyzer.save()

    print()
    print("=" * 60)
    print("NOVA X SOURCE ANALYSIS")
    print("=" * 60)
    print()

    print(
        "Python files:",
        report["summary"]["python_files"]
    )

    print(
        "Functions:",
        report["summary"]["functions"]
    )

    print(
        "Long functions:",
        report["summary"]["long_functions"]
    )

    print()
    print("Saved:")
    print(OUTPUT)
    print()


if __name__ == "__main__":
    main()

