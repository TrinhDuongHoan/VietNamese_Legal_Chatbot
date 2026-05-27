from __future__ import annotations

import json
import re
from pathlib import Path

INPUT_FILES = [
    "../data/embed/law_vi.jsonl",
]
OUTPUT_FILE = "../../backend/data/train.jsonl"


def clean_text(text: str) -> str:
    text = str(text or "")
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def make_question(row: dict) -> str:
    query = clean_text(row.get("query", ""))
    if query:
        return query

    title = clean_text(row.get("title", ""))
    if title:
        return f"Quy định pháp luật về {title} là gì?"

    return "Quy định pháp luật này là gì?"


def make_context(row: dict) -> str:
    for key in ["positive", "context", "content", "text", "body"]:
        value = clean_text(row.get(key, ""))
        if value:
            return value
    return ""


def main() -> None:
    root = Path(__file__).resolve().parent
    out_path = (root / OUTPUT_FILE).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seen = set()
    kept = 0

    with out_path.open("w", encoding="utf-8") as fout:
        for rel in INPUT_FILES:
            in_path = (root / rel).resolve()
            if not in_path.exists():
                print(f"[WARN] Missing {in_path}")
                continue

            with in_path.open("r", encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if not line:
                        continue

                    row = json.loads(line)
                    question = make_question(row)
                    context = make_context(row)

                    if len(question) < 5 or len(context) < 20:
                        continue

                    key = (question, context)
                    if key in seen:
                        continue
                    seen.add(key)

                    fout.write(
                        json.dumps(
                            {"question": question, "context": context},
                            ensure_ascii=False,
                        ) + "\n"
                    )
                    kept += 1

    print(f"[DONE] Saved {kept} rows to {out_path}")


if __name__ == "__main__":
    main()