"""
bpe_tokenizer.py — Sovereign BPE Tokenizer
Clean, deterministic, zero external dependencies.
Prepares text for the C-137 ONNX synthesis contract.

Special tokens live at 256–259 so they never collide with byte IDs 0–255.
Optional merges.txt enables true BPE merges later without API changes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set, Tuple


class SovereignBPE:
    def __init__(self, vocab_path: str | None = None) -> None:
        self.char_to_id: Dict[str, int] = {chr(i): i for i in range(256)}

        self.special: Dict[str, int] = {
            "<pad>": 256,
            "<sos>": 257,
            "<eos>": 258,
            "<unk>": 259,
        }

        self.id_to_char: Dict[int, str] = {v: k for k, v in self.char_to_id.items()}
        self.id_to_char.update({v: k for k, v in self.special.items()})
        self.special_ids: Set[int] = set(self.special.values())

        self.merges: List[Tuple[str, ...]] = []
        if vocab_path and Path(vocab_path).exists():
            self._load_merges(vocab_path)

    def _load_merges(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            self.merges = [
                tuple(line.strip().split()) for line in f if line.strip()
            ]

    def encode(self, text: str, add_special: bool = True) -> List[int]:
        tokens: List[int] = []
        if add_special:
            tokens.append(self.special["<sos>"])
        for c in text:
            tokens.append(self.char_to_id.get(c, self.special["<unk>"]))
        if add_special:
            tokens.append(self.special["<eos>"])
        return tokens

    def decode(self, ids: List[int], skip_special: bool = True) -> str:
        out: List[str] = []
        for i in ids:
            if skip_special and i in self.special_ids:
                continue
            out.append(self.id_to_char.get(i, ""))
        return "".join(out)


tokenizer = SovereignBPE()
