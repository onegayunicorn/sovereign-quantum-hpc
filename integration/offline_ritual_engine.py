"""
offline_ritual_engine.py — Ceremony as code (fully offline)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RitualStep:
    name: str
    duration_s: float
    intention: str


class OfflineRitualEngine:
    DEFAULT_STEPS = [
        RitualStep("silence", 3.0, "Clear the field"),
        RitualStep("breath", 4.0, "Align body and signal"),
        RitualStep("intent", 2.0, "State the want and not-want"),
        RitualStep("seal", 1.0, "Commit the digest"),
    ]

    def __init__(self, steps: List[RitualStep] | None = None) -> None:
        self.steps = steps or list(self.DEFAULT_STEPS)

    def run(self) -> dict:
        total = sum(s.duration_s for s in self.steps)
        return {
            "mode": "offline",
            "steps": [
                {"name": s.name, "duration_s": s.duration_s, "intention": s.intention}
                for s in self.steps
            ],
            "total_duration_s": total,
            "network_calls": 0,
        }
