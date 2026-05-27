from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from datasets import concatenate_datasets, load_dataset

from pipeline_common import DATA_DIR, export_qa_formats, filter_qa_dataframe

DEFAULT_OUTPUT_DIR = DATA_DIR / "finetune_data3"


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


def run(dataset_name: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, int]:
    ds = load_dataset(dataset_name)
    merged = concatenate_datasets([ds[s] for s in ds.keys()]) if len(ds.keys()) > 1 else ds[list(ds.keys())[0]]
    df = merged.to_pandas()

    q_col = _pick_column(df.columns.tolist(), ["question", "query", "prompt", "ask"])
    a_col = _pick_column(df.columns.tolist(), ["answer", "response", "context", "label"])
    if not q_col or not a_col:
        raise ValueError(f"Could not infer question/answer columns from {df.columns.tolist()}")

    working = pd.DataFrame({
        "question": df[q_col],
        "answer": df[a_col],
    })
    for extra in ["title", "source", "category", "law_id", "url"]:
        if extra in df.columns:
            working[extra] = df[extra]

    filtered = filter_qa_dataframe(
        working,
        min_question_len=10,
        min_answer_len=50,
        max_question_len=2000,
        max_answer_len=8000,
    )
    stats = export_qa_formats(filtered, output_dir, "dataset3")
    summary = {
        **stats,
        "rows_before": len(working),
        "rows_after": len(filtered),
    }
    print(summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()
    run(dataset_name=args.dataset, output_dir=Path(args.output_dir))
