import redis
from app.settings import settings

class Memory:
    """
    Handles connection to Redis for shared agent memory.
    """
    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    def set(self, key: str, value: str):
        """Save a value into memory."""
        self.client.set(key, value)

    def get(self, key: str) -> str:
        """Retrieve a value from memory."""
        return self.client.get(key)
        
    def append(self, key: str, value: str):
        """Append to an existing key (creates if not exists)."""
        existing = self.get(key)
        if existing:
            self.set(key, existing + "\n" + value)
        else:
            self.set(key, value)

memory = Memory()
