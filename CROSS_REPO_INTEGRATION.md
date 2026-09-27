# Cross-Repo Integration — Rick C-137 Sovereign Stack

This repository provides the **persona / Council / Genesis / ledger bridge** layer.

| Repository | Role |
|------------|------|
| [the-24ghz-ghost](https://github.com/onegayunicorn/the-24ghz-ghost) | Mathematical core: 5D φ⁵ photonic evolution, 24 GHz portal physics, entity awakening (5 s timeline) |
| [oracle-rick-ai](https://github.com/onegayunicorn/oracle-rick-ai) | Production voice (Piper 22050 Hz), offline oracle, portable apps, Three.js portal UI |
| [rick-c137](https://github.com/onegayunicorn/rick-c137) | Grok skill scaffold (auth, games, UI) |
| **this repo** | `RickC137` engine, Council orchestrator, Genesis loop, UACM ledger |

## Recommended wiring

1. Run `the-24ghz-ghost` simulation → obtain `phase_load` (≈55.45), `awareness`, `entity_state`.
2. Pass those values into `run_rick.py` / `RickC137.inflect()` as `council_consensus` and `genesis_tier`.
3. Send the inflected text to the Piper `/v1/speech` endpoint living in `oracle-rick-ai`.

Shared anchors: φ⁵, 7.83 Hz Schumann, ℓ=3 OAM, 22050 Hz speech.

See `docs/RICK_C137.md` and `integration/rick_c137_engine.py`.
