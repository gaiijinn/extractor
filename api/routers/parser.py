from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from parser_helpers.cleaners.email_cleaner import RemoveDuplicatesEmails
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser.email_extractor import EmailExtractor
from parser_helpers.savers.email_saver import EmailSaver
from typing import List
import os


router = APIRouter(tags=["Parser"])


@router.post("/extract_emails/")
async def extract_emails(
    file: UploadFile = File(...),
    fields: List[str] = Form(...),
):
    try:
        fields = [field.split(",") for field in fields][0]
        file_location = f"./uploads/{file.filename}"
        os.makedirs("./uploads", exist_ok=True)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        parser = CSVMultiReader(fields, file_path=file_location)
        rows = parser.read_file()

        extractor = EmailExtractor(data=rows)
        extractor.process_csv()

        emails = extractor.get_result()

        remover = RemoveDuplicatesEmails(emails)
        data = remover.remove_duplicates()

        saver = EmailSaver(output_file="finals/email.csv", data=data)
        saver.save_result()

        os.remove(file_location)

        return {"status": "success", "emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during email extraction: {str(e)}")