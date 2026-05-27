from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.configs import DEFAULT_COLLECTION_NAME
from src.custom_embedding import get_embedding
from src.search import initialize_search_index
from src.splitter import split_document
from src.vectorize import add_vector, create_collection



def import_qa_data(data_file: str, collection_name: str = DEFAULT_COLLECTION_NAME, batch_size: int = 50, limit: int | None = None) -> dict:
    path = Path(data_file)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    create_collection(collection_name)
    documents_for_search = []
    batch_points = []
    total_rows = 0
    total_chunks = 0

    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            if limit and idx > limit:
                break
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            question = data.get("question", "").strip()
            context = data.get("context", "").strip()
            if not question or not context:
                continue

            total_rows += 1
            documents_for_search.append({
                "question": question,
                "content": context,
                "source": "train",
                "doc_id": idx,
            })

            text = f"{question} {context}"
            nodes = split_document(text)
            for chunk_idx, node in enumerate(nodes, start=1):
                vector = get_embedding(node.text)
                point_id = idx * 1000 + chunk_idx
                batch_points.append({
                    "id": point_id,
                    "vector": vector,
                    "payload": {
                        "question": question,
                        "content": node.text,
                        "source": "train",
                        "doc_id": idx,
                    },
                })
                total_chunks += 1

                if len(batch_points) >= batch_size:
                    add_vector(collection_name, batch_points)
                    batch_points = []

    if batch_points:
        add_vector(collection_name, batch_points)

    initialize_search_index(documents_for_search)
    return {
        "rows": total_rows,
        "chunks": total_chunks,
        "collection": collection_name,
    }



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-file", default="/app/data/train.jsonl")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION_NAME)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    result = import_qa_data(
        data_file=args.data_file,
        collection_name=args.collection,
        batch_size=args.batch_size,
        limit=args.limit,
    )
    print(result)


if __name__ == "__main__":
    main()
