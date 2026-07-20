#!/usr/bin/env python3
"""
===========================================================
NOVA-X Module Base v1.0
===========================================================

Defines the standard interface for all NOVA-X modules.

Every executable module should inherit from ModuleBase
and implement the run(context) method.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from datetime import datetime


class ModuleBase:

    def __init__(self,
                 name,
                 version="1.0",
                 description=""):

        self.name = name
        self.version = version
        self.description = description
        self.created = datetime.now().isoformat(timespec="seconds")

    def run(self, context):
        """
        Override this method in child classes.
        """
        raise NotImplementedError(
            f"{self.name} has not implemented run()."
        )

    def info(self):

        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "created": self.created
        }


############################################################
# Demonstration Module
############################################################

class DemoModule(ModuleBase):

    def __init__(self):

        super().__init__(
            name="Demo Module",
            version="1.0",
            description="Example implementation."
        )

    def run(self, context):

        context.add_execution({

            "module": self.name,
            "status": "SUCCESS"

        })

        print(f"Running {self.name}")

        return context


############################################################

if __name__ == "__main__":

    from pipeline_context import PipelineContext

    context = PipelineContext(

        "Test Module Base"

    )

    module = DemoModule()

    context = module.run(context)

    print()

    print("=" * 60)
    print("MODULE INFORMATION")
    print("=" * 60)

    for key, value in module.info().items():

        print(f"{key:15}: {value}")

    print()

    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    for key, value in context.summary().items():

        print(f"{key:20}: {value}")

