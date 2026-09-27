"""
probability_anchor.py — Probability Machine + Safeguard
Anchors state-space stability; flags runaway drift.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AnchorReading:
    entropy: float
    drift: float
    stable: bool
    message: str


class ProbabilityAnchor:
    def __init__(self, max_drift: float = 0.25) -> None:
        self.max_drift = max_drift
        self.history: List[float] = []

    def observe(self, probability_mass: float) -> AnchorReading:
        p = max(0.0, min(1.0, probability_mass))
        self.history.append(p)
        if len(self.history) < 2:
            return AnchorReading(entropy=0.0, drift=0.0, stable=True, message="primed")

        prev = self.history[-2]
        drift = abs(p - prev)
        if 0 < p < 1:
            import math
            entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        else:
            entropy = 0.0

        stable = drift <= self.max_drift
        return AnchorReading(
            entropy=round(entropy, 4),
            drift=round(drift, 4),
            stable=stable,
            message="anchored" if stable else "drift_exceeded",
        )

    def summary(self) -> Dict[str, float]:
        if not self.history:
            return {"samples": 0}
        return {
            "samples": len(self.history),
            "last": self.history[-1],
            "mean": sum(self.history) / len(self.history),
        }
