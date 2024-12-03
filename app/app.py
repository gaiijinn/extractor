from urllib import request

from fastapi import FastAPI, Depends, Query, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

from parser.email_extractor import EmailExtractor
from parser.email_parser import WebsiteProcessor
from parser_helpers.csv_readers.csv_reader import CSVMultiReader

app = FastAPI()

class ProcessParams(BaseModel):
    threads: int = Query(10, ge=1)
    processes: int = Query(1, ge=1)
    row_names: List[str] = Query(["homepage_url"])


@app.post("/process/")
async def process_file(
    file: UploadFile = File(...),
    params: ProcessParams = Depends()
):
    try:
        file_location = f"./uploads/{file.filename}"
        os.makedirs("./uploads", exist_ok=True)

        with open(file_location, "wb") as f:
            f.write(await file.read())

        csv_reader = CSVMultiReader(file_path=file_location, row_names=params.row_names)
        rows = csv_reader.read_file()

        data = []
        for row in rows:
            for column_name in params.row_names:
                if column_name in row and row[column_name]:
                    data.append(row[column_name])


        processor = WebsiteProcessor(websites=data, threads=params.threads, processes=params.processes)
        result = processor.run()

        os.remove(file_location)

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/extract_emails/")
async def extract_emails(fields: List[str], file: UploadFile = File(...)):
    try:
        file_location = f"./uploads/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        input_path = file_location

        parser = CSVMultiReader(request.fields, file_path=input_path)
        rows = parser.read_file()

        output_file = "../extractor/finals/finalemail_extractor.csv"
        extractor = EmailExtractor(output_file=output_file, data=rows)
        extractor.process_csv()

        results = [{"uuid": row["uuid"], "emails": row.get("emails", [])} for row in extractor.results]

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during email extraction: {str(e)}")


# @app.get("/websites/")
# async def get_websites(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(WebsiteInfo))
#     websites = result.scalars().all()
#     return {"websites": websites}
