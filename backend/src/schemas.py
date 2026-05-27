from pydantic import BaseModel, Field


class CompleteRequest(BaseModel):
    bot_id: str = Field(default="botLawyer")
    user_id: str
    user_message: str
    sync_request: bool = False


class DocumentCreateRequest(BaseModel):
    question: str
    content: str


class HealthResponse(BaseModel):
    status: str
    service: str
