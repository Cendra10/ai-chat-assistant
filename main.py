from fastapi import (FastAPI,
                     HTTPException)
import json
import os
from dotenv import load_dotenv 
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str    

@app.post("/chat/", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = client.chat.completions.create(model="gpc",
                                   messages=[{
                                       "role": "user",
                                       "content":request.message
                                       }]
                                       )
    reply_text = result.choices[0].message.content
    return ChatResponse(reply=reply_text)