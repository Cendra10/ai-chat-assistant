from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str    

class ChatAnalysis(BaseModel):
    summary: str
    sentiment: str