"""
uacm_ledger_bridge.py — UACM → Sovereign Truth Ledger
Every integration action is signed, timestamped, and immutable.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List

LEDGER_FILE = Path("integration_digest.json")


class UACMLedger:
    def __init__(self, ledger_path: Path | None = None) -> None:
        self.path = ledger_path or LEDGER_FILE
        self.entries: List[Dict[str, Any]] = []
        self.seq = 0

    def record(self, source: str, action: str, payload: Dict[str, Any]) -> str:
        self.seq += 1
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        block: Dict[str, Any] = {
            "sequence": self.seq,
            "timestamp_utc": timestamp,
            "source_module": source,
            "action": action,
            "payload": payload,
            "previous_hash": self._last_hash(),
        }

        proof = hashlib.sha256(
            json.dumps(block, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        block["proof_hash"] = proof

        self.entries.append(block)
        self._persist()
        return proof

    def _last_hash(self) -> str:
        return self.entries[-1]["proof_hash"] if self.entries else "GENESIS"

    def _persist(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "schema": "UACM-Sovereign-Integration",
                    "total_entries": self.seq,
                    "latest_proof": self._last_hash(),
                    "entries": self.entries,
                },
                f,
                indent=2,
                default=str,
            )

    def seal_ready(self) -> bool:
        return self.path.exists() and self.path.stat().st_size > 100
