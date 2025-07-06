import httpx
from app.core.config import PDL_API_KEY, PDL_BASE_URL
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

headers = {
    "X-API-Key": PDL_API_KEY,
    "Content-Type": "application/json"
}

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(httpx.RequestError),
    reraise=True
)
async def enrich_company(name: str, website: str):
    url = f"{PDL_BASE_URL}/company/enrich"
    params = {
        "name": name,
        "website": website,
        "min_likelihood": 3,
        "required": "location AND (website OR linkedin_url)"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.get(url, headers=headers, params=params)
            if res.status_code == 404:
                return {"match": False, "reason": "No match found"}
            res.raise_for_status()
            return {"match": True, "data": res.json()}
        except httpx.HTTPStatusError as e:
            logger.warning(f"Enrich failed for {name}: {e.response.status_code} - {e.response.text}")
            return {"match": False, "reason": f"Status error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Unexpected error for {name}: {e}")
            return {"match": False, "reason": str(e)}
