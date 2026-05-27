from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import pandas as pd


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="hf://datasets/anti-ai/ViNLI-Zalo-supervised/law_vi.jsonl.gz",
        help="Đường dẫn file corpus trên Hugging Face",
    )
    parser.add_argument(
        "--output",
        default="../data/embed/law_vi.jsonl",
        help="File output JSONL",
    )
    args = parser.parse_args()

    output_path = (Path(__file__).resolve().parent / args.output).resolve()
    ensure_parent(output_path)

    print(f"[INFO] Reading raw corpus from: {args.source}")

    df = pd.read_json(args.source, lines=True, compression="gzip")

    print(f"[INFO] Loaded {len(df)} raw rows")
    print(f"[INFO] Columns: {list(df.columns)}")

    kept = 0
    with output_path.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            item = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
            text = ""
            for key in ["text", "content", "body", "context", "positive"]:
                val = item.get(key)
                if isinstance(val, str) and val.strip():
                    text = val.strip()
                    break

            if len(text) < 30:
                continue

            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            kept += 1

    print(f"[DONE] Saved {kept} embedding corpus rows to {output_path}")


if __name__ == "__main__":
    main()