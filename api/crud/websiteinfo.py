from sqlalchemy.orm import Session
from fastapi import Depends

from api.db.getdbsession import get_db
from api.db.models import WebsiteInfo


def get_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(WebsiteInfo).offset(skip).limit(limit).all()
    return companies