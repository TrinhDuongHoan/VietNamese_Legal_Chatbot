from __future__ import annotations

import json
from pathlib import Path

from pipeline_common import DATA_DIR, write_jsonl

INPUT_FILES = [
    DATA_DIR / "finetune_data" / "train_instruction_format.jsonl",
    DATA_DIR / "finetune_data" / "test_instruction_format.jsonl",
    DATA_DIR / "finetune_data2" / "vilqa_instruction_format.jsonl",
    DATA_DIR / "finetune_data3" / "dataset3_instruction_format.jsonl",
]
OUTPUT_FILE = DATA_DIR / "merged" / "all_instruction_format.jsonl"


def main() -> None:
    merged = []
    seen = set()
    for path in INPUT_FILES:
        if not path.exists():
            print(f"[WARN] Missing: {path}")
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                key = (row.get("instruction", ""), row.get("input", ""), row.get("output", ""))
                if key in seen:
                    continue
                seen.add(key)
                merged.append(row)
    count = write_jsonl(merged, OUTPUT_FILE)
    print(f"Saved {count} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
