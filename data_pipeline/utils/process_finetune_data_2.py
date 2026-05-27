from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from datasets import load_dataset

from pipeline_common import DATA_DIR, export_qa_formats, filter_qa_dataframe

DEFAULT_DATASET = "huyhuy123/ViLQA"
DEFAULT_OUTPUT_DIR = DATA_DIR / "finetune_data2"


def _pick_column(columns: list[str], candidates: list[str]) -> str | None:
    lowered = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lowered:
            return lowered[cand.lower()]
    for c in columns:
        name = c.lower()
        for cand in candidates:
            if cand.lower() in name:
                return c
    return None


def _dataset_to_dataframe(ds) -> pd.DataFrame:
    parts = []
    for split_name in ds.keys():
        split_df = ds[split_name].to_pandas()
        split_df["split"] = split_name
        parts.append(split_df)
    return pd.concat(parts, ignore_index=True)


def run(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, int]:
    ds = load_dataset(DEFAULT_DATASET)
    df = _dataset_to_dataframe(ds)
    q_col = _pick_column(df.columns.tolist(), ["question", "query", "ask", "prompt"])
    a_col = _pick_column(df.columns.tolist(), ["answer", "response", "context", "label"])
    if not q_col or not a_col:
        raise ValueError(f"Could not infer question/answer columns from {df.columns.tolist()}")

    working = pd.DataFrame({
        "question": df[q_col],
        "answer": df[a_col],
    })
    for extra in ["split", "title", "source", "category", "url"]:
        if extra in df.columns:
            working[extra] = df[extra]

    filtered = filter_qa_dataframe(working)
    stats = export_qa_formats(filtered, output_dir, "vilqa")

    metadata = {
        "dataset": DEFAULT_DATASET,
        "rows_before": int(len(working)),
        "rows_after": int(len(filtered)),
        "columns": df.columns.tolist(),
        "question_column": q_col,
        "answer_column": a_col,
    }
    (output_dir / "vilqa_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    summary = {
        **stats,
        "rows_before": len(working),
        "rows_after": len(filtered),
    }
    print(summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()
    run(output_dir=Path(args.output_dir))
