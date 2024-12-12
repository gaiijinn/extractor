from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from fastapi import Depends

from api.crud.DataWriter import DataWriter
# from api.crud.functions import write_emails_to_db, write_phones_to_db
from api.db.getdbsession import get_db
from api.db.models import Email, WebsiteInfo


def get_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emails = db.query(Email).offset(skip).limit(limit).all()
    return emails


def create_emails_or_phones(rows: List[Dict[str, Optional[Any]]], fields: List[str], db: Session = Depends(get_db)):
    field_map = {field_name: index for index, field_name in enumerate(fields)}

    field_aliases = {
        "email": "emails",
        "phone": "phones",
    }

    if "emails" in fields:
        email_writer = DataWriter(
            db=db,
            fields=fields,
            model=Email,
            field_map=field_map,
            field_aliases=field_aliases,
        )
        email_writer.write_to_db(rows)
    elif "phones" in fields:
        pass
        # phone_writer = DataWriter(
        #     db=db,
        #     fields=fields,
        #     model=Phone,
        #     field_map=field_map,
        #     field_aliases=field_aliases,
        # )
        # phone_writer.write_to_db(rows)
    else:
        raise ValueError("The 'emails' or 'phones' field is required in fields.")