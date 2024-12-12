from fastapi import APIRouter
from fastapi import UploadFile, File, Form, HTTPException, Depends
from typing import List
import os
from sqlalchemy.orm import Session

from api.db.config import SessionLocal
from api.db.models import WebsiteInfo, Email
from parser_helpers.csv_readers.csv_reader import CSVMultiReader



router = APIRouter(tags=["Db"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/emails/")
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emails = db.query(Email).offset(skip).limit(limit).all()
    return emails


@router.post("/write_emails/")
async def write_emails(
    file: UploadFile = File(...),
    fields: List[str] = Form(...),
    db: Session = Depends(get_db),
):
    try:
        fields = [field.split(",") for field in fields][0]
        file_location = f"./uploads/{file.filename}"
        os.makedirs("./uploads", exist_ok=True)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        parser = CSVMultiReader(fields, file_path=file_location)
        rows = parser.read_file()

        for row in rows:
            uuid = row.get(fields[0])
            email = row.get(fields[1])

            if not uuid or not email:
                continue

            website = db.query(WebsiteInfo).filter(WebsiteInfo.uuid == uuid).first()

            if not website:
                continue

            existing_email = db.query(Email).filter(Email.email == email).first()

            if not existing_email:
                new_email = Email(email=email, related_website_id=website.uuid)
                db.add(new_email)

        db.commit()

        os.remove(file_location)
        return {"status": "success", "message": "Emails have been processed and added to the database."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/companies/")
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(WebsiteInfo).offset(skip).limit(limit).all()
    return companies