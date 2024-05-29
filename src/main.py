from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import pandas as pd
import os
from pdf_service import PdfService
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the CSV database
db_path = os.path.join(os.path.dirname(__file__), "../data/database.csv")
df = pd.read_csv(db_path)

# Initialize the PdfService
pdf_service = PdfService("TEST_KEY")

@app.post("/upload/")
async def upload_pdf(company_name: str = Form(...), file: UploadFile = File(...)):
    logger.info("Received request for company: %s", company_name)

    # Check if the company is in the database
    if company_name not in df['Company Name'].values:
        logger.error("Company not found in database: %s", company_name)
        raise HTTPException(status_code=404, detail="Company not found in database")

    # Save the uploaded file temporarily
    temp_file_path = os.path.join(os.path.dirname(__file__), f"../assets/temp.pdf")
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.file.read())

    logger.info("Saved uploaded file to: %s", temp_file_path)

    # Extract data from the PDF using PdfService
    try:
        extracted_data = pdf_service.extract(temp_file_path)
        logger.info("Extracted data: %s", extracted_data)
    except Exception as e:
        logger.error("Error extracting data from PDF: %s", e)
        raise HTTPException(status_code=500, detail=f"Error extracting data from PDF: {e}")

    # Get the data for the company from the CSV database
    db_data = df[df['Company Name'] == company_name].to_dict(orient='records')[0]

    # Compare the data and generate summary
    comparison_result = {}
    for key in db_data.keys():
        comparison_result[key] = {
            "database": db_data[key],
            "extracted": extracted_data.get(key, None),
            "match": db_data[key] == extracted_data.get(key, None)
        }

    # Remove the temporary file
    os.remove(temp_file_path)
    logger.info("Removed temporary file: %s", temp_file_path)

    return JSONResponse(content=comparison_result)
