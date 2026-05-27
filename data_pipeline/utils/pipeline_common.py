from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def clean_text(text: Any) -> str:
    value = str(text or "")
    value = value.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def has_question_mark(question: str) -> bool:
    q = clean_text(question)
    return q.endswith("?") or q.endswith("？")


def normalize_question(question: Any) -> str:
    q = clean_text(question)
    if q and not has_question_mark(q):
        q += "?"
    return q


def normalize_answer(answer: Any) -> str:
    return clean_text(answer)


def keep_qa_pair(
    question: str,
    answer: str,
    *,
    min_question_len: int = 10,
    min_answer_len: int = 50,
    max_question_len: int = 2000,
    max_answer_len: int = 8000,
) -> bool:
    if not question or not answer:
        return False
    if len(question) < min_question_len or len(answer) < min_answer_len:
        return False
    if len(question) > max_question_len or len(answer) > max_answer_len:
        return False
    return True


def dataframe_from_records(records: Iterable[dict[str, Any]]) -> pd.DataFrame:
    rows = list(records)
    if not rows:
        return pd.DataFrame(columns=["question", "answer"])
    return pd.DataFrame(rows)


def write_jsonl(records: Iterable[dict[str, Any]], output_path: Path) -> int:
    ensure_parent(output_path)
    count = 0
    with output_path.open("w", encoding="utf-8") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def export_qa_formats(df: pd.DataFrame, output_dir: Path, prefix: str) -> dict[str, int]:
    ensure_parent(output_dir / "dummy.txt")
    qa_records = []
    instruction_records = []
    conversation_records = []

    for _, row in df.iterrows():
        question = normalize_question(row.get("question", ""))
        answer = normalize_answer(row.get("answer", ""))
        metadata = {
            k: row.get(k)
            for k in df.columns
            if k not in {"question", "answer"}
        }

        qa_records.append({
            "question": question,
            "answer": answer,
            **({"metadata": metadata} if metadata else {}),
        })
        instruction_records.append({
            "instruction": "Bạn là trợ lý pháp luật Việt Nam. Hãy trả lời chính xác, rõ ràng, dễ hiểu.",
            "input": question,
            "output": answer,
            **({"metadata": metadata} if metadata else {}),
        })
        conversation_records.append({
            "messages": [
                {"role": "system", "content": "Bạn là trợ lý pháp luật Việt Nam."},
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer},
            ],
            **({"metadata": metadata} if metadata else {}),
        })

    stats = {}
    stats["qa"] = write_jsonl(qa_records, output_dir / f"{prefix}_qa_format.jsonl")
    stats["instruction"] = write_jsonl(
        instruction_records, output_dir / f"{prefix}_instruction_format.jsonl"
    )
    stats["conversation"] = write_jsonl(
        conversation_records, output_dir / f"{prefix}_conversation_format.jsonl"
    )
    return stats


def filter_qa_dataframe(
    df: pd.DataFrame,
    *,
    min_question_len: int = 10,
    min_answer_len: int = 50,
    max_question_len: int = 2000,
    max_answer_len: int = 8000,
    dedupe: bool = True,
) -> pd.DataFrame:
    working = df.copy()
    if "question" not in working.columns or "answer" not in working.columns:
        raise ValueError("DataFrame must include 'question' and 'answer' columns")

    working["question"] = working["question"].map(normalize_question)
    working["answer"] = working["answer"].map(normalize_answer)

    mask = working.apply(
        lambda row: keep_qa_pair(
            row["question"],
            row["answer"],
            min_question_len=min_question_len,
            min_answer_len=min_answer_len,
            max_question_len=max_question_len,
            max_answer_len=max_answer_len,
        ),
        axis=1,
    )
    working = working[mask].copy()
    if dedupe:
        working = working.drop_duplicates(subset=["question", "answer"]).reset_index(drop=True)
    return working


def build_rag_records_from_qa(df: pd.DataFrame) -> list[dict[str, Any]]:
    records = []
    for _, row in df.iterrows():
        metadata = {
            k: row.get(k)
            for k in df.columns
            if k not in {"question", "answer"}
        }
        record = {
            "question": normalize_question(row.get("question", "")),
            "context": normalize_answer(row.get("answer", "")),
        }
        if metadata:
            record["metadata"] = metadata
        records.append(record)
    return records
