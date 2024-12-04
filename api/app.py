from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from typing import List
import os

from sqlalchemy.orm import Session

from api.db.config import SessionLocal
from api.db.models import WebsiteInfo
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser.email_extractor import EmailExtractor

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/companies/")
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(WebsiteInfo).offset(skip).limit(limit).all()
    return companies


@app.post("/extract_emails/")
async def extract_emails(
    file: UploadFile = File(...),
    fields: List[str] = Form(...),
    output_file: str = Form("finals/investor_email.csv")
):
    try:
        fields = [field.split(",") for field in fields][0]
        file_location = f"./uploads/{file.filename}"
        os.makedirs("./uploads", exist_ok=True)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        parser = CSVMultiReader(fields, file_path=file_location)
        rows = parser.read_file()

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        extractor = EmailExtractor(output_file=output_file, data=rows)
        extractor.process_csv()

        emails = extractor.get_result()

        os.remove(file_location)

        return {"status": "success", "emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during email extraction: {str(e)}")