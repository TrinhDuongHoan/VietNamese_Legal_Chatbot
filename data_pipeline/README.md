# Data pipeline

Thư mục này dựng lại phần chuẩn bị dữ liệu của repo gốc theo hướng dễ chạy hơn và nhất quán schema hơn.

## Mục tiêu

- Tải corpus pháp luật cho RAG
- Tải các bộ dữ liệu Q&A để fine-tune
- Chuẩn hóa mọi dữ liệu về format thống nhất
- Xuất ra các format:
  - `qa_format.jsonl`
  - `instruction_format.jsonl`
  - `conversation_format.jsonl`
  - `backend/data/train.jsonl` cho backend import vào Qdrant

## Cấu trúc

```text
data_pipeline/
├── data/
│   ├── embed/
│   │   └── law_vi.jsonl
│   ├── finetune_data/
│   ├── finetune_data2/
│   ├── finetune_data3/
│   └── merged/
└── utils/
    ├── pipeline_common.py
    ├── download_embed_data.py
    ├── download_embed_data.ipynb
    ├── process_finetune_data.py
    ├── process_finetune_data.ipynb
    ├── process_finetune_data_2.py
    ├── process_finetune_data_2.ipynb
    ├── process_finetune_data_3.py
    ├── process_finetune_data_3.ipynb
    ├── merge_instruction_data.py
    └── normalize_rag_schema.py
```

## Cài dependencies

```bash
pip install -r data_pipeline/requirements.txt
```

## Bước 1: tải corpus pháp luật cho RAG

```bash
cd data_pipeline/utils
python download_embed_data.py
```

Kết quả: `data_pipeline/data/embed/law_vi.jsonl`

Bạn cũng có thể truyền file local:

```bash
python download_embed_data.py --input-path ../data/raw/law_vi.jsonl.gz
```

## Bước 2: tạo dataset fine-tune số 1

```bash
cd data_pipeline/utils
python process_finetune_data.py
```

Kết quả nằm trong `data_pipeline/data/finetune_data/`:
- `train_qa_format.jsonl`
- `train_instruction_format.jsonl`
- `train_conversation_format.jsonl`
- `test_qa_format.jsonl`
- `test_instruction_format.jsonl`
- `test_conversation_format.jsonl`
- `train_rag_format.jsonl`

## Bước 3: tạo dataset fine-tune số 2

```bash
cd data_pipeline/utils
python process_finetune_data_2.py
```

Kết quả nằm trong `data_pipeline/data/finetune_data2/`:
- `vilqa_qa_format.jsonl`
- `vilqa_instruction_format.jsonl`
- `vilqa_conversation_format.jsonl`
- `vilqa_metadata.json`

## Bước 4: tạo dataset fine-tune số 3

```bash
cd data_pipeline/utils
python process_finetune_data_3.py --dataset some-owner/some-dataset
```

Kết quả nằm trong `data_pipeline/data/finetune_data3/`:
- `dataset3_qa_format.jsonl`
- `dataset3_instruction_format.jsonl`
- `dataset3_conversation_format.jsonl`

## Bước 5: gộp instruction data

```bash
cd data_pipeline/utils
python merge_instruction_data.py
```

Kết quả: `data_pipeline/data/merged/all_instruction_format.jsonl`

## Bước 6: chuẩn hóa sang format backend RAG

Backend hiện import ổn định nhất với schema:

```json
{"question": "...", "context": "..."}
```

Tạo file này bằng lệnh:

```bash
cd data_pipeline/utils
python normalize_rag_schema.py
```

Kết quả được ghi sang:

```text
backend/data/train.jsonl
```

## Chạy bằng notebook

Nếu muốn chạy bằng Jupyter, mở từng notebook trong `utils/`:
- `download_embed_data.ipynb`
- `process_finetune_data.ipynb`
- `process_finetune_data_2.ipynb`
- `process_finetune_data_3.ipynb`

Các notebook này gọi trực tiếp các file `.py` tương ứng, nên bạn có thể debug trong notebook rồi đem logic đó chạy bằng terminal.
