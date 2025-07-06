from fastapi import APIRouter, HTTPException
from app.services.research import research_startups
from app.models.startup import StartupRequest

router = APIRouter()

@router.post("/submit-startups")
async def submit_startups(payload: StartupRequest):
    if not payload.startups:
        raise HTTPException(status_code=400, detail="No startups provided")

    startup_entries = [startup.model_dump() for startup in payload.startups]
    results = await research_startups(startup_entries)
    return {"results": results}