import subprocess
import os
from app.settings import settings

class ShellTool:
    """Execute shell commands safely within the workspace."""
    def __init__(self):
        self.workspace = os.path.abspath(settings.WORKSPACE_ROOT)

    def execute(self, command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
            return output if output else "Command executed successfully (no output)."
        except subprocess.TimeoutExpired:
            return "Error: Command timed out."
        except Exception as e:
            return f"Error executing command: {e}"
