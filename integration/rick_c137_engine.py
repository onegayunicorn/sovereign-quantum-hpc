"""
rick_c137_engine.py — RICK C-137 PERSONA ENGINE
Layered text inflection + optional ONNX runner.
Integrates with Council consensus + Genesis tier.

NOTE: This is a *persona / mel-stub* layer for the sovereign-quantum-hpc stack.
The production speech path for the Oracle lives in oracle-rick-ai
(Piper ONNX mono 16-bit 22050 Hz + personality DSP). Real weights for this
Tacotron-style graph are optional and separate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import numpy as np

try:
    import onnxruntime as ort

    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    ort = None  # type: ignore

PERSONA_VECTOR = np.array(
    [
        0.82, 0.91, 0.76, 0.88, 0.65, 0.93, 0.70, 0.85,
        0.60, 0.78, 0.83, 0.90, 0.55, 0.81, 0.74, 0.86,
        0.42, 0.38, 0.51, 0.45, 0.60, 0.55, 0.48, 0.52,
        0.35, 0.40, 0.58, 0.44, 0.50, 0.47, 0.53, 0.41,
        0.95, 0.88, 0.45, 0.32, 0.90, 0.28, 0.85, 0.50,
        0.92, 0.35, 0.80, 0.40, 0.87, 0.30, 0.94, 0.65,
        0.783, 0.618, 0.99, 0.97, 0.84, 0.92, 0.88, 0.95,
        0.76, 0.89, 0.93, 0.81, 0.96, 0.85, 0.91, 1.00,
    ],
    dtype=np.float32,
).reshape(1, 64)


class RickC137:
    """C-137 persona — filter text through the voice before synthesis."""

    def __init__(self, model_path: str = "models/rick_c137.onnx") -> None:
        self.model_path = Path(model_path)
        self.session: Optional["ort.InferenceSession"] = None
        self.persona = PERSONA_VECTOR.copy()
        self.phase = "CALIBRATING"
        self.energy_level = 0.0

        if ONNX_AVAILABLE and self.model_path.exists():
            try:
                self._load_session()
                self.phase = "ACTIVE"
            except Exception as e:
                print(f"[C137] ONNX load failed — SIMULATED ({e})")
                self.phase = "SIMULATED"
        else:
            self.phase = "SIMULATED"

    def _load_session(self) -> None:
        assert ort is not None
        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
        self.session = ort.InferenceSession(
            str(self.model_path),
            sess_options=opts,
            providers=["CPUExecutionProvider"],
        )
        input_names = [i.name for i in self.session.get_inputs()]
        if "text_tokens" not in input_names:
            print(f"[C137] warn: expected input 'text_tokens', got {input_names}")

    def inflect(
        self,
        text: str,
        council_consensus: float = 0.75,
        genesis_tier: float = 1.0,
    ) -> Tuple[str, np.ndarray]:
        emphasis = float(council_consensus)
        if genesis_tier == float("inf"):
            drawl_factor = 0.618
        else:
            drawl_factor = 1.0 / max(1.0, float(genesis_tier) / 3.0)

        persona_mod = self.persona.copy()
        persona_mod[:, 16:20] *= drawl_factor
        persona_mod[:, 32:36] *= 0.5 + emphasis / 2.0

        modulated = text
        if emphasis > 0.85:
            modulated = f"*clears throat* {modulated} — and let me tell ya..."
        if genesis_tier == float("inf"):
            modulated = f"Look, I've been around this loop before. {modulated}"

        return modulated, persona_mod

    def synthesize(
        self, text_tokens: np.ndarray, persona_vec: np.ndarray
    ) -> np.ndarray:
        if self.session is None:
            return (np.random.randn(80, 100).astype(np.float32) * 0.1 + 0.5)

        feeds = {}
        names = {i.name for i in self.session.get_inputs()}
        if "text_tokens" in names:
            feeds["text_tokens"] = text_tokens.reshape(1, -1).astype(np.int64)
        if "persona_vec" in names:
            feeds["persona_vec"] = persona_vec.astype(np.float32)

        result = self.session.run(None, feeds)
        out = result[0]
        if out.ndim == 1:
            out = out.reshape(80, -1) if out.size >= 80 else out.reshape(1, -1)
        return out.astype(np.float32)

    def status_dict(self) -> dict:
        return {
            "identity": "RICK_C137",
            "phase": self.phase,
            "onnx_loaded": self.session is not None,
            "onnxruntime": ONNX_AVAILABLE,
            "persona_dim": list(self.persona.shape),
            "anchor_frequency_hz": 7.83,
            "golden_anchor": 1.618,
            "sovereign_local_only": True,
            "note": "Production speech: oracle-rick-ai Piper path; this is persona/mel layer",
        }
