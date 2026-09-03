from fastapi import (FastAPI,
                     HTTPException)
import json
import os
from dotenv import load_dotenv 
from pydantic import BaseModel
from openai import OpenAI
from datetime import datetime

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
            tools=tools
            )
    
    message = result.choices[0].message
    if message.tool_calls:
        function_name = message.tool_calls[0].function.name
        print(function_name)

        if function_name == "get_current_time":
            tool_result = get_current_time()

        history.append({
            "role": "tool",
            "tool_call_id": message.tool_calls[0].id,
            "name": function_name,
            "content": tool_result
            })
        
        result = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=history,
            tools=tools
            )
        reply_text = result.choices[0].message.content
        history.append({"role": "assistant", "content": reply_text})
        return ChatResponse(reply=reply_text)
    else:
        reply_text = message.content
        history.append({"role": "assistant", "content": reply_text})
        return ChatResponse(reply=reply_text)


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

tools = [
    {
        "type": "function",
        "function":{
            "name":"get_current_time",
            "description": "Mengambil waktu saat ini dalam format HH:MM:SS",
            "parameters":{
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]