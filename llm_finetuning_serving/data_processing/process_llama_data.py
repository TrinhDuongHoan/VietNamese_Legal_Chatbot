import json
from pathlib import Path

INPUT_FILE = "../backend/data/train.jsonl"
OUTPUT_FILE = "llm_finetuning_serving/data_processing/processed_llama_data.jsonl"


def main():
    out = Path(OUTPUT_FILE)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(INPUT_FILE, "r", encoding="utf-8") as fin, out.open("w", encoding="utf-8") as fout:
        for line in fin:
            item = json.loads(line)
            record = {
                "messages": [
                    {"role": "system", "content": "Bạn là trợ lý pháp luật Việt Nam."},
                    {"role": "user", "content": item["question"]},
                    {"role": "assistant", "content": item["context"]},
                ]
            }
            fout.write(json.dumps(record, ensure_ascii=False) + "")

if __name__ == "__main__":
    main()
