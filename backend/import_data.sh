#!/usr/bin/env bash
set -e
python -m src.import_data --data-file /app/data/train.jsonl --collection llm --batch-size 50
