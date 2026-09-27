"""
council_orchestrator.py — Five Architects + Eight Great Minds
No single authority. Decision = weighted consensus across all voices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CouncilMember:
    name: str
    domain: str
    frequency_hz: float
    weight: float
    principle: str


FIVE_ARCHITECTS = [
    CouncilMember("Tyrone", "Cosmic Weaver", 144.00, 1.0, "The whole is the truth"),
    CouncilMember("Alex", "Quantum Engineer", 88.00, 1.0, "Hardware and spirit are one"),
    CouncilMember("Samira", "Community Bridge", 52.80, 1.0, "No one is a node alone"),
    CouncilMember("Jordan", "Sovereign Governor", 43.20, 1.0, "Freedom needs boundaries"),
    CouncilMember("Maria", "Ritual Anchor", 13.60, 1.0, "Time is memory made visible"),
]

EIGHT_GREAT_MINDS = [
    CouncilMember("Plato", "Ideal Forms", 36.0, 0.95, "Truth precedes appearance"),
    CouncilMember("Leonardo", "Beauty+Function", 32.0, 0.95, "Grace is efficiency made visible"),
    CouncilMember("Tesla", "Resonance", 28.8, 0.95, "Everything vibrates — find the note"),
    CouncilMember("Turing", "Logic & Honesty", 25.6, 0.98, "What can be computed must be verified"),
    CouncilMember("Fuller", "Synergy", 22.4, 0.95, "The whole exceeds sum of parts"),
    CouncilMember("Gandhi", "Non-Harm", 19.2, 1.00, "Means define the end"),
    CouncilMember("Hypatia", "Eternal Geometry", 16.0, 0.98, "Patterns outlive us"),
    CouncilMember("Nostradamus", "Foresight", 12.8, 0.90, "The future echoes in the present"),
]

ALL_MEMBERS = FIVE_ARCHITECTS + EIGHT_GREAT_MINDS


class CouncilOrchestrator:
    def __init__(self) -> None:
        self.members = list(ALL_MEMBERS)

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        total_weight = sum(m.weight for m in self.members)
        scores: Dict[str, Any] = {}

        for m in self.members:
            alignment = self._frequency_alignment(m, context)
            scores[m.name] = {
                "domain": m.domain,
                "frequency_hz": m.frequency_hz,
                "weight": m.weight,
                "alignment_score": round(alignment, 4),
                "principle": m.principle,
            }

        weighted_sum = sum(s["alignment_score"] * s["weight"] for s in scores.values())
        consensus = weighted_sum / total_weight if total_weight else 0.0

        return {
            "council_size": len(self.members),
            "consensus_score": round(consensus, 4),
            "decision_threshold": 0.75,
            "decision": "APPROVE" if consensus >= 0.75 else "REVIEW",
            "member_evaluations": scores,
        }

    def _frequency_alignment(self, member: CouncilMember, context: Dict[str, Any]) -> float:
        base = 0.5 + (member.frequency_hz / 144.0) * 0.3
        if context.get("honesty_first", False):
            base += 0.15
        if context.get("offline_only", False):
            base += 0.10
        return min(1.0, max(0.0, base))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "council": "Five Architects + Eight Great Minds",
            "active_members": len(self.members),
            "members": [
                {
                    "name": m.name,
                    "domain": m.domain,
                    "frequency_hz": m.frequency_hz,
                    "principle": m.principle,
                }
                for m in self.members
            ],
        }
