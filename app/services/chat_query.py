from app.core.openai import call_openai
from app.core.database import AsyncSessionLocal
from sqlalchemy import text

EXAMPLE_SCHEMA = """
Table: companies
Columns:

id (integer)
name (string)
website (string)
source (string)
summary (string)
industry (string)
size (string)
employee_count (integer)
founded (integer)
location (string)
city (string)
country (string)
linkedin_url (string)
facebook_url (string)
twitter_url (string)
type (string)
ticker (string)
alternative_names (json)
tags (json)
funding_total (integer)
funding_stage (string)
last_funding_date (string)
funding_rounds (integer)
employee_count_by_country (json)
raw_json (json)

Primary Key:
id

Unique Constraint:
website

Indexes:
ix_companies_id (id)
"""

SYSTEM_PROMPT = f"""
You're a SQL assistant. Given a user question and this schema:

{EXAMPLE_SCHEMA}

Output only a valid SQLite SQL query. Do not explain.
"""

async def nl_to_sql(nl_query: str) -> str:
    prompt = f"User: {nl_query}"
    sql = await call_openai(prompt, system_prompt=SYSTEM_PROMPT)
    return sql.strip().strip("```sql").strip("```")

async def execute_sql(sql: str) -> list[dict]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(sql))
        rows = result.mappings().all()
        return [dict(row) for row in rows]
