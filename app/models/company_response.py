from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class CompanyLocation(BaseModel):
    name: Optional[str]
    locality: Optional[str]
    region: Optional[str]
    country: Optional[str]
    street_address: Optional[str]
    postal_code: Optional[str]
    geo: Optional[str]

    class Config:
        extra = "allow"


class CompanyData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    display_name: Optional[str]
    size: Optional[str]
    employee_count: Optional[int]
    founded: Optional[int]
    industry: Optional[str]
    location: Optional[CompanyLocation]
    linkedin_url: Optional[str]
    facebook_url: Optional[str]
    twitter_url: Optional[str]
    type: Optional[str]  # public/private
    ticker: Optional[str]
    alternative_names: Optional[List[str]]
    tags: Optional[List[str]]
    summary: Optional[str]
    total_funding_raised: Optional[int]
    latest_funding_stage: Optional[str]
    last_funding_date: Optional[str]
    number_funding_rounds: Optional[int]
    employee_count_by_country: Optional[Dict[str, int]]

    class Config:
        extra = "allow"  # store anything else in `.raw_json` if needed


class CompanyResult(BaseModel):
    match: bool
    data: Optional[CompanyData]
