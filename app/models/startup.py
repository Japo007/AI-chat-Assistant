from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class StartupEntry(BaseModel):
    name: str
    website: HttpUrl

class StartupRequest(BaseModel):
    startups: List[StartupEntry]