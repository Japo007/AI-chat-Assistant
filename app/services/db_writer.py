from app.models.company import Company
from app.core.database import AsyncSessionLocal
from app.models.company_response import CompanyResult
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

async def save_company(result: CompanyResult):

    data = result.data
    location = data.location or {}

    async with AsyncSessionLocal() as session:
        try:
            company = Company(
                name=data.name,
                website=str(data.website),
                source="PDL",
                summary=data.summary,
                industry=data.industry,
                size=data.size,
                employee_count=data.employee_count,
                founded=data.founded,
                location=location.name if location else None,
                city=location.locality if location else None,
                country=location.country if location else None,
                linkedin_url=data.linkedin_url,
                facebook_url=data.facebook_url,
                twitter_url=data.twitter_url,
                type=data.type,
                ticker=data.ticker,
                alternative_names=data.alternative_names,
                tags=data.tags,
                funding_total=data.total_funding_raised,
                funding_stage=data.latest_funding_stage,
                last_funding_date=data.last_funding_date,
                funding_rounds=data.number_funding_rounds,
                employee_count_by_country=data.employee_count_by_country,
                raw_json=data.dict()
            )

            session.add(company)
            await session.commit()
            logger.info(f"Saved company: {company.name}")
        except IntegrityError:
            await session.rollback()
            logger.warning(f"Company already exists: {result.website}")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error saving company {result.startup}: {str(e)}")
        finally:
            await session.close()
