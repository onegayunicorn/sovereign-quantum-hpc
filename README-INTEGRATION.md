# Sovereign Integration Layer

Binds Council (5 Architects + 8 Minds), EPTT pressure transduction, Genesis want/not-want loop, probability anchor, offline ritual, and UACM ledger digest.

## Layout

```
integration/
  council_orchestrator.py
  pressure_transducer.py
  genesis_loop.py
  uacm_ledger_bridge.py
  probability_anchor.py
  offline_ritual_engine.py
run_integration.py
```

## Run

```bash
python3 run_integration.py
# → integration_digest.json (hash-chained entries)
```

## Notes

- Fully offline; no network calls.
- Ledger proofs are SHA-256 truncations of sorted JSON blocks.
- Consensus threshold default: 0.75.
- Sacred Codex tiers 0–9 and ∞ when truth is high and want > not_want.

This is a **symbolic orchestration / audit layer**, not a replacement for physical sensors or cryptographic HSM sealing.
