import asyncio
import logging
from typing import List

from app.services.pdl_client import enrich_company
from app.services.db_writer import save_company
from app.models.company_response import CompanyResult


logger = logging.getLogger(__name__)

async def research_startup(name: str, website: str) -> dict:
    result = await enrich_company(name, website)

    if result["match"]:
        # Persist to DB
        try:
            await save_company(CompanyResult(**result))
            logger.info(f"Saved company to DB: {name}")
        except Exception as e:
            logger.error(f"Failed to save company {name}: {e}")
    else:
        logger.warning(f"No match for {name}: {result.get('reason')}")

    return {
        "startup": name,
        "website": website,
        "match": result["match"],
        "data": result.get("data", {}),
        "reason": result.get("reason")
    }

async def research_startups(startup_entries: List[dict]) -> List[dict]:
    tasks = [research_startup(entry["name"], entry["website"]) for entry in startup_entries]
    return await asyncio.gather(*tasks)