# models/rick_c137

## Spec (manifest — not weights)

| Field | Value |
|-------|--------|
| Inputs | `text_tokens` int64[batch, seq], `persona_vec` float32[batch, 64] |
| Output | `mel_out` float32[80, frames] |
| Sample rate target | 22050 Hz |

### Persona vector layout

| Range | Role |
|-------|------|
| [0..15] | Tone / Sarcasm / Weariness |
| [16..31] | Rhythm / Pace / Drawl |
| [32..47] | Conviction / Cynicism / Heart |
| [48..63] | Sovereign anchor (7.83 Hz / φ) |

```bash
pip install onnx onnxruntime numpy
python3 scripts/create_rick_onnx_stub.py
```

`models/*.onnx` is **gitignored**. Production speech for the Oracle remains **oracle-rick-ai Piper** path.
