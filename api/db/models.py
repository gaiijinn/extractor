from sqlalchemy import Column, String, Text, UUID, Integer, Boolean, ForeignKey
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


class Email(Base):
    __tablename__ = "file_loader_email"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    related_website_id = Column(PgUUID(as_uuid=True), ForeignKey("file_loader_websiteinfo.uuid"), nullable=False)