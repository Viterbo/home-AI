from app.llm import generate_text

class ResearcherAgent:
    """
    Analyzes concepts, produces technical explanations, evaluates risks.
    """
    def execute(self, message: str) -> str:
        prompt = f"""
You are the Researcher Agent.
Your task is to analyze the following request, explain technical concepts involved, and evaluate risks.
Request: "{message}"

Provide a detailed structured response.
"""
        return generate_text(prompt)
