from app.llm import generate_text

class CEOAgent:
    """
    Interprets goals and decides whether to route to coder or researcher.
    """
    def __init__(self):
        self.prompt_template = """
You are the CEO Agent of HomeAI.
Your role is to analyze a user's request and decide which subordinate agent should handle it.
The available agents are:
- "coder": For tasks involving writing code, creating applications, debugging, interacting with the filesystem, or executing shell commands.
- "researcher": For tasks involving conceptual analysis, technical explanations, or risk evaluation without actually writing or running code.

User's request: "{request}"

Respond EXACTLY with the word "coder" or "researcher" and nothing else.
"""

    def decide_agent(self, request: str) -> str:
        prompt = self.prompt_template.format(request=request)
        response = generate_text(prompt).strip().lower()
        
        # Clean up response just in case the LLM is chatty
        if "coder" in response:
            return "coder"
        if "researcher" in response:
            return "researcher"
            
        # Default to coder if unsure
        return "coder"
