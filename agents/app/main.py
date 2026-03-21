import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew
from crewai import LLM

# =========================
# CONFIG
# =========================

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# =========================
# LOGGING
# =========================

def console_log(label: str, data: any = ""):
    sys.stderr.write(f"[{label}] {data}\n")
    sys.stderr.flush()

# =========================
# LLM (CREWAI COMPATIBLE)
# =========================

console_log("INIT", "Initializing CrewAI Ollama LLM")

llm = LLM(
    model=f"ollama/{MODEL}" if not MODEL.startswith("ollama/") else MODEL,
    base_url=OLLAMA_URL,
)

# =========================
# AGENTS
# =========================

console_log("INIT", "Creating agents")

coder = Agent(
    role="Senior Developer",
    goal="Write and explain code",
    backstory="Expert software engineer",
    verbose=True,
    llm=llm
)

poet = Agent(
    role="Poet",
    goal="Write beautiful poetry",
    backstory="Romantic and creative poet",
    verbose=True,
    llm=llm
)

# =========================
# FASTAPI
# =========================

app = FastAPI()

class TaskRequest(BaseModel):
    message: str

@app.post("/tasks")
async def run_task(req: TaskRequest):
    try:
        console_log("REQUEST.IN", req.message)

        selected_agent = coder if "code" in req.message.lower() else poet
        console_log("AGENT.SELECTED", selected_agent.role)

        task = Task(
            description=req.message,
            expected_output="A complete response",
            agent=selected_agent
        )

        console_log("TASK.CREATED", req.message)

        crew = Crew(
            agents=[coder, poet],
            tasks=[task],
            verbose=True,
            tracing=True
        )

        console_log("CREW.START", "Executing crew")

        result = crew.kickoff()

        console_log("CREW.RESULT", str(result)[:200])

        return {"result": str(result)}

    except Exception as e:
        console_log("ERROR", str(e))
        raise