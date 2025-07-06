from fastapi import APIRouter, HTTPException
from app.models.chat_request import ChatRequest
from app.services.chat_query import nl_to_sql, execute_sql
import logging
from app.services.query_cache import get_cached_response, save_cached_response
import json

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat-query")
async def chat_query(request: ChatRequest):
    # Check cache
    cached = await get_cached_response(request.query.strip())
    if cached:
        return {
            "query": request.query,
            "result": json.loads(cached)
        }
    try:
        sql = await nl_to_sql(request.query)
        result = await execute_sql(sql)
        await save_cached_response(request.query.strip(), result)
        return {
            "query": request.query,
            "sql": sql,
            "result": result
        }
    except Exception as e:
        logger.error(f"Failed to process chat query '{request.query}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred while processing your query.")
