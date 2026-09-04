from fastapi import FastAPI
import os
from dotenv import load_dotenv 
from schemas import (ChatRequest, ChatResponse, ChatAnalysis)
from tools import get_current_time, tools
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

@app.post("/chat/", response_model=ChatResponse)
def chat(request: ChatRequest):
    global history
    history.append({"role": "user", "content": request.message})
    
    result = client.chat.completions.create(
        model="openai/gpt-oss-20b",
            messages=history,
            tools=tools,
            stream=True
    )

    reply_text = ""
    tool_call_id = None
    function_name = ""
    function_args = ""

    for chunk in result:
        delta = chunk.choices[0].delta
        if delta.content:
            reply_text += delta.content
        if delta.tool_calls:
            tc = delta.tool_calls[0]
            if tc.id:
                tool_call_id = tc.id
            if tc.function.name:
                function_name += tc.function.name
            if tc.function.arguments:
                function_args += tc.function.arguments
    if function_name:
        if function_name == "get_current_time":
            tool_result = get_current_time()

        history.append({
            "role": "assistant",
            "tool_calls":[{
                "id": tool_call_id,
                "type": "function",
                "function": {"name": function_name, "arguments": function_args}
            }]
        })

        history.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": function_name,
            "content": tool_result
        })

        result2 = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=history,
            tools=tools
        )
        reply_text = result2.choices[0].message.content
        history.append({"role": "assistant", "content": reply_text})
        return ChatResponse(reply=reply_text)
    else:
        history.append({"role": "assistant", "content": reply_text})
        return ChatResponse(reply=reply_text)

@app.post("/analyze/", response_model=ChatAnalysis)
def analyze(request: ChatRequest):
    result = client.chat.completions.parse(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": request.message}],
        response_format=ChatAnalysis
    )
    return result.choices[0].message.parsed