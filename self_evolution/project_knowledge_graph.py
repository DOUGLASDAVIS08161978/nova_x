#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
NOVA X PROJECT KNOWLEDGE GRAPH v1.0
Architecture Discovery Engine
═══════════════════════════════════════════════════════════════════════════════

This module is READ ONLY.

Purpose:
    • Discover project structure
    • Record module dependencies
    • Record classes and functions
    • Build a reusable architecture graph

No source files are modified.
"""

from pathlib import Path
from datetime import datetime, UTC
import ast
import json

OUTPUT = Path("self_evolution/reports/project_knowledge_graph.json")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


class ModuleVisitor(ast.NodeVisitor):

    def __init__(self):
        self.imports = []
        self.classes = []
        self.functions = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        self.imports.append(module)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)


class KnowledgeGraph:

    def __init__(self):
        self.graph = {
            "generated": datetime.now(UTC).isoformat(),
            "modules": [],
            "summary": {}
        }

    def analyze(self, path):

        try:

            source = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            visitor = ModuleVisitor()
            visitor.visit(tree)

            return {
                "file": str(path),
                "imports": sorted(set(visitor.imports)),
                "classes": sorted(visitor.classes),
                "functions": sorted(visitor.functions)
            }

        except Exception as exc:

            return {
                "file": str(path),
                "error": str(exc)
            }

    def build(self):

        pyfiles = sorted(Path(".").rglob("*.py"))

        total_imports = 0
        total_classes = 0
        total_functions = 0

        for file in pyfiles:

            if "__pycache__" in str(file):
                continue

            result = self.analyze(file)

            self.graph["modules"].append(result)

            total_imports += len(result.get("imports", []))
            total_classes += len(result.get("classes", []))
            total_functions += len(result.get("functions", []))

        self.graph["summary"] = {
            "modules": len(self.graph["modules"]),
            "imports": total_imports,
            "classes": total_classes,
            "functions": total_functions
        }

        return self.graph

    def save(self):

        graph = self.build()

        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4)

        return graph


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

    kg = KnowledgeGraph()

    graph = kg.save()

    print()
    print("=" * 60)
    print("NOVA X PROJECT KNOWLEDGE GRAPH")
    print("=" * 60)
    print()

    for key, value in graph["summary"].items():
        print(f"{key:12} : {value}")

    print()
    print("Saved:")
    print(OUTPUT)
    print()


if __name__ == "__main__":
    main()

