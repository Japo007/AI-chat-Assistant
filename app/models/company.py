from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=False, unique=True)
    source = Column(String, default="PDL")
    summary = Column(String)
    industry = Column(String)
    size = Column(String)
    employee_count = Column(Integer)
    founded = Column(Integer)
    location = Column(String)
    city = Column(String)
    country = Column(String)
    linkedin_url = Column(String)
    facebook_url = Column(String)
    twitter_url = Column(String)
    type = Column(String)  # public/private
    ticker = Column(String)  # optional for public companies
    alternative_names = Column(JSON)  # aliases
    tags = Column(JSON)
    funding_total = Column(Integer)
    funding_stage = Column(String)
    last_funding_date = Column(String)
    funding_rounds = Column(Integer)
    employee_count_by_country = Column(JSON)
    raw_json = Column(JSON)