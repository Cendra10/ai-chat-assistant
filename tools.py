from datetime import datetime

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