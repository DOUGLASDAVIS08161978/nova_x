#!/usr/bin/env python3
"""
===========================================================
NOVA-X Pipeline Context v1.0
===========================================================

Shared execution context passed between NOVA-X modules.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from datetime import datetime


class PipelineContext:

    def __init__(self, goal):

        self.goal = goal

        self.created = datetime.now().isoformat(timespec="seconds")

        self.plan = []

        self.execution_report = []

        self.capability_gaps = []

        self.generated_tools = []

        self.innovations = []

        self.score = None

        self.metadata = {}

    def set_plan(self, plan):

        self.plan = plan

    def add_execution(self, result):

        self.execution_report.append(result)

    def add_gap(self, gap):

        self.capability_gaps.append(gap)

    def add_generated_tool(self, tool):

        self.generated_tools.append(tool)

    def add_innovation(self, item):

        self.innovations.append(item)

    def set_score(self, score):

        self.score = score

    def summary(self):

        return {

            "goal": self.goal,

            "created": self.created,

            "plan_steps": len(self.plan),

            "executions": len(self.execution_report),

            "capability_gaps": len(self.capability_gaps),

            "generated_tools": len(self.generated_tools),

            "innovations": len(self.innovations),

            "score": self.score

        }


############################################################

if __name__ == "__main__":

    context = PipelineContext(

        "Demonstrate shared execution context."

    )

    context.set_plan([

        "Plan task",

        "Execute task",

        "Evaluate task"

    ])

    context.add_execution({

        "step": 1,

        "status": "SUCCESS"

    })

    context.add_gap("PDF Reader")

    context.add_generated_tool("PDFReader")

    context.add_innovation("Improve PDF extraction")

    context.set_score(100)

    print()

    print("=" * 60)

    print("NOVA-X PIPELINE CONTEXT")

    print("=" * 60)

    print()

    for key, value in context.summary().items():

        print(f"{key:20}: {value}")
