# AI Startup Research Assistant

A full-stack FastAPI backend that:
- Accepts startup names + websites
- Enriches them using People Data Labs (PDL)
- Stores results to SQLite
- Allows querying results via natural language using OpenAI GPT
- Caches past queries, uses retries, rate limits, structured logging, and follows clean architecture principles

---

## Features

- Async FastAPI + httpx
- GPT-4o powered chat-to-SQL endpoint
- SQLite + SQLAlchemy ORM
- Retry logic for OpenAI + PDL
- Rate limiting and exception handling
- Logging + Debugging in VSCode
- `.env` based secrets
- Query caching using SHA256 hashes with TTL

---

## Project Setup (Local Dev)

```bash
git clone https://github.com/Japo007/AI-chat-Assistant
cd ai-startup-research-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# .env
PDL_API_KEY=your_pdl_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

Running the app: uvicorn app.main:app --reload

Open your browser and visit: uvicorn app.main:app --reload
```

## API Endpoints
```json
Request: 
{
  "startups": [
    { "name": "Figma", "website": "https://www.figma.com" },
    { "name": "Notion", "website": "https://www.notion.so" }
  ]
}

Response:
{
  "results": [
    {
      "startup": "Figma",
      "website": "https://www.figma.com",
      "match": true,
      "data": {
        "summary": "...",
        "linkedin_url": "linkedin.com/company/figma"
      }
    }
  ]
}

Request:
{
  "prompt": "List all startups and their LinkedIn URLs"
}

Response:
{
  "result": [
    { "name": "Figma", "linkedin_url": "linkedin.com/company/figma" }
  ]
}
```
