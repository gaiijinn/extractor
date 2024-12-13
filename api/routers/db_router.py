from fastapi import APIRouter
from fastapi import UploadFile, File, Form, HTTPException, Depends
from typing import List
import os
from api.crud import websiteinfo
from api.crud import email
from sqlalchemy.orm import Session

from api.db.getdbsession import get_db
from parser_helpers.csv_readers.csv_reader import CSVMultiReader



router = APIRouter(tags=["Db"])


@router.get("/emails/")
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return email.get_emails(skip=skip, limit=limit, db=db)


@router.post("/write_emails/")
async def write_emails(
    file: UploadFile = File(...),
    fields: List[str] = Form(...),
    db: Session = Depends(get_db),
):
    try:
        fields = [field.split(",") for field in fields][0]
        if 'uuid' not in fields:
            raise HTTPException(status_code=400, detail="The 'uuid' field is required in fields.")
        file_location = f"./uploads/{file.filename}"
        os.makedirs("./uploads", exist_ok=True)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        parser = CSVMultiReader(fields, file_path=file_location)
        rows = parser.read_file()

        email.create_emails_or_phones(fields=fields, rows=rows, db=db)

        os.remove(file_location)
        return {"status": "success", "message": "Emails have been processed and added to the database."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/companies/")
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return websiteinfo.get_companies(skip=skip, limit=limit, db=db)