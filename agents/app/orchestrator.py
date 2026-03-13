from app.agents.ceo_agent import CEOAgent
from app.agents.coder_agent import CoderAgent
from app.agents.researcher_agent import ResearcherAgent

class AgentOrchestrator:
    """
    Receives tasks and coordinates execution through the CEO agent.
    """
    def __init__(self):
        self.ceo = CEOAgent()
        self.agents = {
            "coder": CoderAgent(),
            "researcher": ResearcherAgent()
        }

    async def run_task(self, message: str) -> tuple[str, str]:
        """
        Runs a task by first consulting the CEO to pick an agent,
        then delegating the task to that agent.
        """
        # CEO decides what agent to use
        selected_agent_name = self.ceo.decide_agent(message)
        
        selected_agent = self.agents.get(selected_agent_name)
        if not selected_agent:
            return selected_agent_name, f"Error: Agent '{selected_agent_name}' not implemented or invalid."
            
        # Execute task with chosen agent
        result = selected_agent.execute(message)
        
        return selected_agent_name, result
