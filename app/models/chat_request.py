from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    query: str