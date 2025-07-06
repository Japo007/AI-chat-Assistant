import hashlib
from datetime import datetime, timedelta
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.query_cache import QueryCache
import logging
import json

logger = logging.getLogger(__name__)

CACHE_TTL_MINUTES = 60 * 24  # 1 day

def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.strip().encode()).hexdigest()

async def get_cached_response(prompt: str) -> str | None:
    prompt_hash = hash_prompt(prompt)
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(QueryCache).where(QueryCache.prompt_hash == prompt_hash))
        record = result.scalar_one_or_none()
        if record:
            if record.expires_at and datetime.utcnow() > record.expires_at:
                logger.info(f"Cache expired: {prompt_hash}")
                return None
            logger.info(f"Cache hit: {prompt_hash}")
            return record.response
        logger.info(f"Cache miss: {prompt_hash}")
        return None

async def save_cached_response(prompt: str, response: str):
    prompt_hash = hash_prompt(prompt)
    expires_at = datetime.utcnow() + timedelta(minutes=CACHE_TTL_MINUTES)
    if isinstance(response, (dict, list)):
        response = json.dumps(response)
    async with AsyncSessionLocal() as session:
        record = QueryCache(
            prompt=prompt,
            prompt_hash=prompt_hash,
            response=response,
            expires_at=expires_at
        )
        session.add(record)
        await session.commit()
        logger.info(f"Cached new query: {prompt_hash}")
