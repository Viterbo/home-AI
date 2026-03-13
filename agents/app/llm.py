import requests
from app.settings import settings

def generate_text(prompt: str) -> str:
    """
    Communicates with local Ollama to generate text.
    """
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LLM: {str(e)}"
