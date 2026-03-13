from app.llm import generate_text
from app.tools.filesystem_tool import FilesystemTool
from app.tools.shell_tool import ShellTool

class CoderAgent:
    """
    Produces development plans, generates code, interacts with workspace.
    """
    def __init__(self):
        self.fs = FilesystemTool()
        self.shell = ShellTool()

    def execute(self, message: str) -> str:
        prompt = f"""
You are the Coder Agent. 
Your task is to fulfill the user's request: "{message}"

Since this is a simple mockup implementation, provide a development plan, and specify the commands or file writes you WOULD do.
Currently, I am acting autonomously but simply returning the response.

Please answer with your code or plan.
"""
        response = generate_text(prompt)
        
        # In a full advanced implementation, this agent would iterate through thoughts/actions.
        # For this version, we format a response and maybe run a dummy fs command to show it works.
        files_in_workspace = self.fs.list_dir("")
        
        return f"Coder Agent Plan:\n{response}\n\nWorkspace contents:\n{files_in_workspace}"
