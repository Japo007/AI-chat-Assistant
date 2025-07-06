from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QueryCache(Base):
    __tablename__ = "query_cache"

    id = Column(Integer, primary_key=True, index=True)
    prompt_hash = Column(String(64), unique=True, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    expires_at = Column(DateTime()) 
