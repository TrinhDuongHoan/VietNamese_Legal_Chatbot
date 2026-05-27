# Vietnamese Legal Chatbot RAG System - Rebuild

Đây là bản dựng lại đầy đủ, nhất quán hơn của repo gốc `Vietnamese-Legal-Chatbot-RAG-System`.

## Thành phần
- FastAPI backend
- Celery worker
- MariaDB
- Valkey/Redis-compatible broker
- Qdrant vector database
- Streamlit frontend
- Data pipeline để chuẩn hóa dữ liệu sang `train.jsonl`
- Module fine-tuning/serving mẫu
- Embed serving mẫu
- Tests, scripts, docs

## Kiến trúc
1. `data_pipeline` tải/xử lý dữ liệu, rồi chuẩn hóa về `backend/data/train.jsonl`.
2. `backend/src/import_data.py` đọc `train.jsonl`, chunk text, sinh embedding, upsert vào Qdrant và build search index.
3. Frontend gửi câu hỏi tới `POST /chat/complete`.
4. Celery worker route câu hỏi sang legal RAG, tools, web search hoặc general chat.
5. Nếu là legal RAG, hệ thống retrieve context, rerank, build prompt rồi gọi LLM.
6. Kết quả được lưu vào MariaDB.

## Chạy nhanh
```bash
cp .env.example .env
docker compose up -d --build
curl -X POST http://localhost:8000/data/import
```

Mở:
- Backend docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

Xem `docs/deployment.md` để biết hướng dẫn chi tiết.
