#!/usr/bin/env python3
"""
run_rick.py — COUNCIL → GENESIS → C-137 VOICE → SEAL
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))


def text_to_tokens(text: str) -> np.ndarray:
    return np.array([ord(c) % 256 for c in text], dtype=np.int64)


def main() -> int:
    print("=" * 70)
    print("  RICK C-137 SOVEREIGN VOICE PIPELINE")
    print("  Council → Genesis → Persona → Synthesis → Seal")
    print("=" * 70)

    try:
        from integration.council_orchestrator import CouncilOrchestrator
        from integration.genesis_loop import GenesisLoop
        from integration.uacm_ledger_bridge import UACMLedger
    except ImportError as e:
        print(f"[warn] integration modules missing: {e}")
        return 1

    from integration.rick_c137_engine import RickC137

    ledger = UACMLedger()

    print("\n[1/5] Council Deliberation...")
    council = CouncilOrchestrator()
    context = {"honesty_first": True, "offline_only": True, "c137_anchor": True}
    c_result = council.evaluate(context)
    consensus = c_result["consensus_score"]
    print(f"  Consensus: {consensus} → {c_result['decision']}")

    print("\n[2/5] Genesis Loop — Want / Not-Want...")
    loop = GenesisLoop()
    s = loop.iterate(want=0.94, not_want=0.88)
    tier_label = "∞" if s.tier == float("inf") else s.tier
    print(f"  Truth: {s.truth} | Tier: {tier_label}")
    message = loop.codex_phase()
    print(f"  Message: {message}")

    print("\n[3/5] C-137 Persona Inflection...")
    rick = RickC137()
    spoken, persona_vec = rick.inflect(message, consensus, s.tier)
    print(f"  Phase: {rick.phase}")
    print(f"  As spoken: {spoken}")

    print("\n[4/5] ONNX / Simulated Synthesis...")
    tokens = text_to_tokens(spoken)
    mel = rick.synthesize(tokens, persona_vec)
    mode = "ONNX live" if rick.session else "simulated"
    print(f"  Mel shape: {mel.shape} — {mode}")

    print("\n[5/5] UACM Seal...")
    proof = ledger.record(
        "C137_VOICE",
        "pipeline_complete",
        {
            "council_consensus": consensus,
            "genesis_truth": s.truth,
            "tier": "INFINITY" if s.tier == float("inf") else s.tier,
            "spoken_text": spoken,
            "synthesis_mode": rick.phase,
            "mel_bands": int(mel.shape[0]) if mel.ndim > 0 else 0,
            "mel_frames": int(mel.shape[1]) if mel.ndim > 1 else int(mel.size),
            "persona_anchor": "7.83Hz-phi",
        },
    )
    print(f"  Proof: {proof}")

    print("\n" + "=" * 70)
    print("  C-137 Pipeline Complete — Voice Sealed")
    print("  Digest: integration_digest.json")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
