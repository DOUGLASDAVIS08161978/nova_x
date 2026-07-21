#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
NOVA X INTROSPECTION ENGINE v1.0
Human-in-the-Loop Self Analysis
═══════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
from datetime import datetime, UTC
import ast
import json

REPORT_DIR = Path("self_evolution/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        end_line = getattr(node, "end_lineno", node.lineno)
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "length": end_line - node.lineno + 1
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        end_line = getattr(node, "end_lineno", node.lineno)
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "length": end_line - node.lineno + 1
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)


class IntrospectionEngine:

    def __init__(self):
        self.report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "files": [],
            "summary": {}
        }

    def scan_file(self, path):

        try:
            source = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            visitor = FunctionVisitor()
            visitor.visit(tree)

            todos = 0
            fixmes = 0

            for line in source.splitlines():
                upper = line.upper()

                if "TODO" in upper:
                    todos += 1

                if "FIXME" in upper:
                    fixmes += 1

            long_functions = [
                f for f in visitor.functions
                if f["length"] > 75
            ]

            return {
                "file": str(path),
                "functions": len(visitor.functions),
                "classes": len(visitor.classes),
                "todos": todos,
                "fixmes": fixmes,
                "long_functions": long_functions
            }

        except Exception as exc:

            return {
                "file": str(path),
                "error": str(exc)
            }

    def run(self):

        pyfiles = sorted(Path(".").rglob("*.py"))

        total_functions = 0
        total_classes = 0
        total_todos = 0
        total_fixmes = 0
        long_count = 0

        for file in pyfiles:

            if "__pycache__" in str(file):
                continue

            result = self.scan_file(file)

            self.report["files"].append(result)

            total_functions += result.get("functions", 0)
            total_classes += result.get("classes", 0)
            total_todos += result.get("todos", 0)
            total_fixmes += result.get("fixmes", 0)
            long_count += len(result.get("long_functions", []))

        self.report["summary"] = {
            "python_files": len(pyfiles),
            "functions": total_functions,
            "classes": total_classes,
            "todos": total_todos,
            "fixmes": total_fixmes,
            "long_functions": long_count
        }

        return self.report

    def save(self):

        report = self.run()

        outfile = REPORT_DIR / "introspection_report.json"

        with open(outfile, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        return outfile, report


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
"""
Auto-generated docstring for main.
"""

    engine = IntrospectionEngine()

    outfile, report = engine.save()

    print()
    print("=" * 60)
    print("NOVA X INTROSPECTION REPORT")
    print("=" * 60)
    print()

    for key, value in report["summary"].items():
        print(f"{key:20} : {value}")

    print()
    print("Saved report to:")
    print(outfile)
    print()


if __name__ == "__main__":
    main()
