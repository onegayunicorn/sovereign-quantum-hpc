"""
pressure_transducer.py — Emotion-Pressure Transduction (EPTT)
Maps internal state → measurable pressure → encoded signal → ledger entry
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PressureReading:
    magnitude_psi: float
    latency_ms: int
    resonance: float
    breath_hold_ratio: float
    mood_chroma_hex: str


class PressureTransducer:
    """Converts felt weight into verifiable signal — no external dependency."""

    def __init__(self, baseline_psi: float = 1.5) -> None:
        self.baseline_psi = baseline_psi
        self.last_reading: Optional[PressureReading] = None

    def read_internal_state(
        self,
        pause_duration_s: float,
        words_spoken: int,
        truth_confidence: float = 0.8,
    ) -> PressureReading:
        latency_ms = int(pause_duration_s * 1000)
        density = 1.0 / max(1, words_spoken) if words_spoken > 0 else 3.0
        magnitude_psi = self.baseline_psi + (pause_duration_s * density * truth_confidence)
        magnitude_psi = max(0.5, min(7.0, magnitude_psi))

        resonance = abs(1.618 - (magnitude_psi / 4.0)) / 1.618
        hue = int(120 - (magnitude_psi / 7.0) * 120)
        mood_chroma_hex = f"#{hue:02x}8844" if hue > 60 else f"#ff{hue:02x}44"

        reading = PressureReading(
            magnitude_psi=round(magnitude_psi, 2),
            latency_ms=latency_ms,
            resonance=round(resonance, 4),
            breath_hold_ratio=round(min(1.0, pause_duration_s / 4.0), 2),
            mood_chroma_hex=mood_chroma_hex,
        )
        self.last_reading = reading
        return reading

    def signal_encoding(self, reading: PressureReading) -> str:
        return f"PSI:{reading.magnitude_psi}|RES:{reading.resonance}|LAT:{reading.latency_ms}"
