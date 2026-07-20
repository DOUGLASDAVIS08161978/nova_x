#!/usr/bin/env python3
"""
===========================================================
NOVA-X Execution Pipeline v1.0
===========================================================

Coordinates execution across registered modules.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from pipeline_context import PipelineContext
from module_registry import ModuleRegistry


class ExecutionPipeline:

    def __init__(self, registry):

        self.registry = registry

    def execute(self, context):

        print()
        print("=" * 60)
        print("BEGINNING EXECUTION PIPELINE")
        print("=" * 60)
        print()

        enabled = self.registry.enabled_modules()

        for index, name in enumerate(enabled.keys(), start=1):

            print(f"[{index}/{len(enabled)}] {name}")

            context.add_execution({

                "module": name,

                "status": "SUCCESS"

            })

        context.set_score(100)

        print()
        print("=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)

        return context


############################################################

if __name__ == "__main__":

    registry = ModuleRegistry()

    registry.register("Task Planner")
    registry.register("Task Executor")
    registry.register("Execution History")
    registry.register("Self Evaluation")
    registry.register("Capability Analyzer")
    registry.register("Tool Architect")
    registry.register("Tool Generator")
    registry.register("Innovation Queue")

    registry.disable("Execution History")

    context = PipelineContext(

        "Demonstrate execution pipeline."

    )

    pipeline = ExecutionPipeline(registry)

    context = pipeline.execute(context)

    print()
    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    for key, value in context.summary().items():

        print(f"{key:20}: {value}")
