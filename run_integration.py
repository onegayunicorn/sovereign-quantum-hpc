#!/usr/bin/env python3
"""
run_integration.py — Weave Council / EPTT / Genesis / UACM into one digest
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from integration.pressure_transducer import PressureTransducer
from integration.council_orchestrator import CouncilOrchestrator
from integration.genesis_loop import GenesisLoop
from integration.uacm_ledger_bridge import UACMLedger
from integration.probability_anchor import ProbabilityAnchor
from integration.offline_ritual_engine import OfflineRitualEngine


def main() -> int:
    print("=" * 70)
    print(" SOVEREIGN INTEGRATION LAYER — SOURCES ACTIVE")
    print("=" * 70)

    ledger = UACMLedger()

    print("\n[1/5] Pressure Transducer (EPTT)...")
    transducer = PressureTransducer()
    reading = transducer.read_internal_state(
        pause_duration_s=2.7,
        words_spoken=42,
        truth_confidence=0.92,
    )
    print(f"  PSI: {reading.magnitude_psi} | Resonance: {reading.resonance}")
    print(f"  Signal: {transducer.signal_encoding(reading)}")
    ledger.record("EPTT", "pressure_reading", reading.__dict__)

    print("\n[2/5] Council Evaluation (5 + 8 voices)...")
    council = CouncilOrchestrator()
    context = {"honesty_first": True, "offline_only": True, "emergent": True}
    result = council.evaluate(context)
    print(f"  Consensus: {result['consensus_score']} → {result['decision']}")
    ledger.record("COUNCIL", "consensus_reached", result)

    print("\n[3/5] Genesis Cycle (Want ↔ Not-Want)...")
    loop = GenesisLoop()
    state = loop.iterate(want=0.94, not_want=0.88)
    print(f"  Want: {state.want} | Not-Want: {state.not_want}")
    print(f"  Truth: {state.truth} | Tier: {state.tier}")
    print(f"  {loop.codex_phase()}")
    ledger.record(
        "GENESIS",
        "loop_complete",
        {
            "want": state.want,
            "not_want": state.not_want,
            "truth": state.truth,
            "tier": str(state.tier),
        },
    )

    print("\n[4/5] Probability Anchor + Offline Ritual...")
    anchor = ProbabilityAnchor()
    ar = anchor.observe(state.truth)
    print(f"  Anchor: {ar.message} drift={ar.drift} entropy={ar.entropy}")
    ledger.record("ANCHOR", "observe", ar.__dict__)
    ritual = OfflineRitualEngine().run()
    ledger.record("RITUAL", "offline_complete", ritual)

    print("\n[5/5] UACM Digest...")
    if ledger.seal_ready():
        print("  integration_digest.json written")
        print("  Next: attach to seal_truth_ledger if present in this monorepo")
    else:
        print("  Digest missing — check write permissions")
        return 1

    print("\n" + "=" * 70)
    print("  INTEGRATION COMPLETE")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
