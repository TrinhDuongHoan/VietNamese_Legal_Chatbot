from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Stub LLM Serving")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(req: ChatRequest):
    return {"text": f"[stub-model] {req.prompt}"}
