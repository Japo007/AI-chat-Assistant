import os
import logging
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from tenacity import retry, wait_random_exponential, stop_after_attempt, RetryError
import httpx

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Retry OpenAI API 3 times with exponential backoff
@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
async def _safe_openai_call(messages: list[ChatCompletionMessageParam]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

# Main call function with fallback
async def call_openai(user_prompt: str, system_prompt: str = None) -> str:
    messages: list[ChatCompletionMessageParam] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    try:
        return await _safe_openai_call(messages)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning("Rate limited by OpenAI (429). Falling back.")
            return fallback_sql_response(user_prompt)
    except RetryError as e:
        logger.error("OpenAI failed after retries. Falling back.")
        return fallback_sql_response(user_prompt)
    except Exception as e:
        logger.exception("OpenAI call crashed")
        return fallback_sql_response(user_prompt)
    
def fallback_sql_response(user_prompt: str) -> str:
    lowered = user_prompt.lower()
    if "employee count" in lowered:
        return "SELECT name, employee_count FROM companies ORDER BY employee_count DESC LIMIT 10"
    elif "total" in lowered and "funding" in lowered:
        return "SELECT SUM(funding_total) AS total_funding FROM companies"
    elif "all" in lowered or "list" in lowered:
        return "SELECT name, website FROM companies LIMIT 50"
    else:
        return "SELECT name, website, country FROM companies LIMIT 10"
