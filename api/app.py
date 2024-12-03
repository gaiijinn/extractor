from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import os
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser.email_extractor import EmailExtractor

app = FastAPI()

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