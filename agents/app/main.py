from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.orchestrator import AgentOrchestrator

app = FastAPI(title="HomeAI Agents API")
orchestrator = AgentOrchestrator()

class TaskRequest(BaseModel):
    message: str

class TaskResponse(BaseModel):
    selected_agent: str
    result: str

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """
    Main endpoint to receive tasks.
    Delegates the task to the Orchestrator.
    """
    try:
        selected_agent, result = await orchestrator.run_task(request.message)
        return TaskResponse(selected_agent=selected_agent, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
