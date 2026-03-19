import sys
import os
import requests
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# =========================
# CONFIG
# =========================

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

MEMORY_KEY = "agent_memory"
MAX_MEMORY_CHARS = 4000

# =========================
# LOGGING (INFALIBLE)
# =========================

def console_log(label: str, data: any = ""):
    sys.stderr.write(f"[{label}] {data}\n")
    sys.stderr.flush()

# =========================
# REDIS
# =========================

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_memory():
    console_log("REDIS.GET", MEMORY_KEY)
    return redis_client.get(MEMORY_KEY) or ""

def append_memory(text: str):
    console_log("REDIS.APPEND", text[:100])

    existing = get_memory()
    new_value = existing + "\n" + text

    # trim memory
    if len(new_value) > MAX_MEMORY_CHARS:
        new_value = new_value[-MAX_MEMORY_CHARS:]

    redis_client.set(MEMORY_KEY, new_value)

# =========================
# LLM
# =========================

def call_llm(prompt: str) -> str:
    console_log("LLM.PROMPT", prompt[:300])

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        result = data.get("response", "")
        console_log("LLM.RESPONSE", result[:300])
        return result
    except Exception as e:
        console_log("LLM.ERROR", str(e))
        return f"Error: {e}"

# =========================
# FASTAPI
# =========================

app = FastAPI(title="HomeAI Single Agent Test")

class TaskRequest(BaseModel):
    message: str

class TaskResponse(BaseModel):
    result: str

# =========================
# ENDPOINT
# =========================

@app.post("/tasks", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    try:
        console_log("REQUEST.IN", request.message)

        # 1. load memory
        memory = get_memory()
        console_log("MEMORY.LOADED", memory[:200])

        # 2. build prompt
        prompt = f"""
You are a persistent AI agent.

Previous conversation:
{memory}

New message:
{request.message}

Instructions:
- Continue the conversation
- Use previous context
- Be consistent
"""

        # 3. call LLM
        response = call_llm(prompt)

        # 4. save memory
        append_memory(f"User: {request.message}")
        append_memory(f"Agent: {response}")

        console_log("REQUEST.OUT", response[:200])

        return TaskResponse(result=response)

    except Exception as e:
        console_log("ERROR", str(e))
        raise HTTPException(status_code=500, detail=str(e))