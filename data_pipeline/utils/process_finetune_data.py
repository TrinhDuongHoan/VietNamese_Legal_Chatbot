from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from datasets import load_dataset

from pipeline_common import (
    DATA_DIR,
    build_rag_records_from_qa,
    export_qa_formats,
    filter_qa_dataframe,
    write_jsonl,
)

DEFAULT_DATASET = "phuocsang/hoidap-tvpl-20k"
DEFAULT_OUTPUT_DIR = DATA_DIR / "finetune_data"


def _to_dataframe(split) -> pd.DataFrame:
    return split.to_pandas()


def run(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, int]:
    ds = load_dataset(DEFAULT_DATASET)
    train_df = _to_dataframe(ds["train"])
    test_df = _to_dataframe(ds["test"])

    train_filtered = filter_qa_dataframe(
        train_df,
        min_question_len=10,
        min_answer_len=50,
        max_answer_len=5000,
    )
    test_filtered = filter_qa_dataframe(
        test_df,
        min_question_len=10,
        min_answer_len=50,
        max_answer_len=5000,
    )

    train_stats = export_qa_formats(train_filtered, output_dir, "train")
    test_stats = export_qa_formats(test_filtered, output_dir, "test")

    rag_count = write_jsonl(
        build_rag_records_from_qa(train_filtered),
        output_dir / "train_rag_format.jsonl",
    )

    summary = {
        "train_rows": len(train_filtered),
        "test_rows": len(test_filtered),
        "train_qa": train_stats["qa"],
        "train_instruction": train_stats["instruction"],
        "train_conversation": train_stats["conversation"],
        "test_qa": test_stats["qa"],
        "test_instruction": test_stats["instruction"],
        "test_conversation": test_stats["conversation"],
        "train_rag": rag_count,
    }
    print(summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()
    run(output_dir=Path(args.output_dir))
