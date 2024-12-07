from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.dialects.postgresql import UUID as PgUUID
import uuid

from api.db.config import Base


class WebsiteInfo(Base):
    __tablename__ = "file_loader_websiteinfo"
    uuid = Column(PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    cb_url = Column(Text, nullable=True)
    homepage_url = Column(Text)
    facebook_url = Column(Text, nullable=True)
    twitter_url = Column(Text, nullable=True)
    linkedin_url = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    country_code = Column(String(100), nullable=True)