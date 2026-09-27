#!/usr/bin/env python3
"""Create a minimal ONNX stub for models/rick_c137.onnx (local only, gitignored)."""

from __future__ import annotations

from pathlib import Path

import onnx
from onnx import TensorProto, helper


def main() -> None:
    out = Path("models/rick_c137.onnx")
    out.parent.mkdir(parents=True, exist_ok=True)

    X = helper.make_tensor_value_info("text_tokens", TensorProto.INT64, ["batch", "seq"])
    P = helper.make_tensor_value_info("persona_vec", TensorProto.FLOAT, ["batch", 64])
    Y = helper.make_tensor_value_info("mel_out", TensorProto.FLOAT, [80, "frames"])

    gather = helper.make_node(
        "ReduceMean",
        ["persona_vec"],
        ["persona_mean"],
        name="C137_PersonaMean",
        keepdims=1,
    )
    cast = helper.make_node(
        "Cast",
        ["text_tokens"],
        ["tokens_f"],
        name="C137_Cast",
        to=TensorProto.FLOAT,
    )
    identity = helper.make_node(
        "Identity",
        ["tokens_f"],
        ["mel_out"],
        name="C137_Stub",
    )

    graph = helper.make_graph(
        [gather, cast, identity],
        "rick_c137",
        [X, P],
        [Y],
    )
    model = helper.make_model(graph, producer_name="Sovereign-C137")
    model.opset_import[0].version = 13
    onnx.checker.check_model(model)
    onnx.save(model, str(out))
    print(f"stub written: {out}")


if __name__ == "__main__":
    main()
