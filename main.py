from fastapi import (FastAPI,
                     HTTPException)
import json
import os
from dotenv import load_dotenv 
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
app = FastAPI()
history = [
    {"role": "system", "content": "Kamu adalah asisten yang ramah dan menjawab singkat dalam Bahasa Indonesia."}
]

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str    

@app.post("/chat/", response_model=ChatResponse)
def chat(request: ChatRequest):
    global history
    history.append({"role": "user", "content": request.message})
    
    result = client.chat.completions.create(
        model="openai/gpt-oss-20b",
            messages=history,
            stream=True
            )

    reply_text = ""
    for chunk in result: 
        delta = chunk.choices[0].delta.content
        if delta:
            reply_text += delta
    
    history.append({"role": "assistant", "content": reply_text})
    return ChatResponse(reply=reply_text)