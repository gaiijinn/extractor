from sqlalchemy import Column, Integer, String, UUID, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WebsiteInfo(Base):
    __tablename__ = "app_websiteinfo"

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    cb_url = Column(Text, nullable=True)
    homepage_url = Column(Text, nullable=False)
    facebook_url = Column(Text, nullable=True)
    twitter_url = Column(Text, nullable=True)
    linkedin_url = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    country_code = Column(String(100), nullable=True)