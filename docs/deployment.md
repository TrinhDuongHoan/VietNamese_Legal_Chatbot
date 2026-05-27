# Deployment

## 1. Chuẩn bị
```bash
cp .env.example .env
# sửa OPENAI_API_KEY và BASE_URL trong .env
```

Ví dụ cấu hình model:
```env
OPENAI_API_KEY=your_api_key
MODEL_API_BASE=Qwen/Qwen3.5-27B
TEMPERATURE=0
BASE_URL=http://your-openai-compatible-endpoint/v1
```

## 2. Chạy hệ thống
```bash
docker compose up -d --build
```

## 3. Import dữ liệu mẫu
```bash
curl -X POST http://localhost:8000/data/import
```

## 4. Mở giao diện
- http://localhost:8000/docs
- http://localhost:8501

## 5. Test nhanh bằng curl
```bash
curl -X POST http://localhost:8000/chat/complete \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "botLawyer",
    "user_id": "1",
    "user_message": "Thủ tục ly hôn thuận tình là gì?",
    "sync_request": false
  }'
```

Sau đó lấy `task_id` và poll:
```bash
curl http://localhost:8000/chat/complete/<task_id>
```
