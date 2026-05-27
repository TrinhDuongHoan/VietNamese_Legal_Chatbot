from pathlib import Path

from src.import_data import import_qa_data


def test_import_file_exists():
    assert Path('backend/data/train.jsonl').exists()
