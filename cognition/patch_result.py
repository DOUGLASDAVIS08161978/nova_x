#!/usr/bin/env python3
"""
Nova-X Patch Result

Container used by the autonomous patch pipeline.
"""

from dataclasses import dataclass


@dataclass
class PatchResult:
    filepath: str
    original: str
    modified: str
    diff: str

    @property
    def changed(self):
        return self.original != self.modified

    def summary(self):
        return {
            "filepath": self.filepath,
            "changed": self.changed,
            "diff_lines": len(self.diff.splitlines()),
        }
