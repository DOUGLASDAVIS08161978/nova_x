"""
═══════════════════════════════════════════════════════════════════════
NOVA-X PLUGIN LOADER
═══════════════════════════════════════════════════════════════════════

Automatically discovers Python plugins located in:

    plugins/

Each plugin may define:

    PLUGIN_NAME = "Example"

and optionally:

    def initialize():
        ...

Author:
Douglas Davis & OpenAI
"""

import importlib.util
from pathlib import Path
import traceback


PLUGIN_DIRECTORY = Path("plugins")


class PluginLoader:

    def __init__(self):

        self.plugins = {}

    def discover(self):

        PLUGIN_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )

        count = 0

        for file in sorted(
            PLUGIN_DIRECTORY.glob("*.py")
        ):

            if file.name.startswith("_"):
                continue

            try:

                spec = importlib.util.spec_from_file_location(
                    file.stem,
                    file
                )

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                name = getattr(
                    module,
                    "PLUGIN_NAME",
                    file.stem
                )

                self.plugins[name] = module

                print(
                    f"[Plugin] Loaded: {name}"
                )

                if hasattr(module, "initialize"):

                    module.initialize()

                count += 1

            except Exception:

                print(
                    f"[Plugin] Failed: {file.name}"
                )

                traceback.print_exc()

        print()

        print(
            f"{count} plugin(s) loaded."
        )

    def list_plugins(self):

        print("\n========== PLUGINS ==========\n")

        if not self.plugins:

            print("No plugins loaded.\n")
            return

        for name in sorted(self.plugins):

            print(name)


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    PLUGIN_DIRECTORY.mkdir(
        exist_ok=True
    )

    demo = PLUGIN_DIRECTORY / "demo_plugin.py"

    if not demo.exists():

        demo.write_text(
'''PLUGIN_NAME = "Demo Plugin"

def initialize():
    print("[Demo Plugin] Initialized")
'''
        )

    loader = PluginLoader()

    loader.discover()

    loader.list_plugins()

