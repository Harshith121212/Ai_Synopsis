from dotenv import load_dotenv  # Import from python-dotenv
from pymongo import MongoClient
from PyPDF2 import PdfReader
import json
import os
import gridfs  # Import gridfs from pymongo

load_dotenv()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_CONNECTION_URI")
client = MongoClient(MONGO_URI)
db = client["pdf_database"]  # Database name
collection = db["pdf_files"]  # Collection name
fs = gridfs.GridFS(db)  # Using gridfs from pymongo

# Upload PDF to MongoDB using GridFS
def upload_pdf_to_mongodb(uploaded_file):
    try:
        # Save the file to GridFS
        file_id = fs.put(uploaded_file, filename=uploaded_file.name)
        print(f"File uploaded to MongoDB with GridFS ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file to MongoDB: {e}")
        return None

# Extract text from PDF
def extract_text_from_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Save the extracted text to a JSON file
def save_text_to_json(extracted_text, output_file="preprocessed.json"):
    json_data = {"content": extracted_text}
    with open(output_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Extracted text saved to {output_file}")
    return output_file

# Retrieve a PDF from MongoDB using GridFS (if needed)
def retrieve_pdf_from_mongodb(file_id):
    try:
        # Retrieve the file from GridFS using the file_id
        file_data = fs.get(file_id)
        with open(file_data.filename, "wb") as f:
            f.write(file_data.read())
        print(f"File retrieved and saved as {file_data.filename}")
    except Exception as e:
        print(f"Error retrieving file from MongoDB: {e}")
