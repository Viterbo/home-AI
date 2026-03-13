import os
from app.settings import settings

class FilesystemTool:
    """Read/write/list files limited to the workspace."""
    def __init__(self):
        self.workspace = os.path.abspath(settings.WORKSPACE_ROOT)

    def _safe_path(self, path: str) -> str:
        """Ensure the path is within the workspace."""
        # Remove leading slashes if path is accidentally absolute over workspace
        if path.startswith("/"):
            path = path.lstrip("/")
        full_path = os.path.abspath(os.path.join(self.workspace, path))
        if not full_path.startswith(self.workspace):
            raise ValueError(f"Access denied: {path} is outside the workspace.")
        return full_path

    def read_file(self, path: str) -> str:
        try:
            safe_path = self._safe_path(path)
            with open(safe_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {path}: {e}"

    def write_file(self, path: str, content: str) -> str:
        try:
            safe_path = self._safe_path(path)
            os.makedirs(os.path.dirname(safe_path), exist_ok=True)
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file {path}: {e}"

    def list_dir(self, path: str = "") -> str:
        try:
            safe_path = self._safe_path(path)
            items = os.listdir(safe_path)
            return "\n".join(items) if items else "Empty directory"
        except Exception as e:
            return f"Error listing directory {path}: {e}"
