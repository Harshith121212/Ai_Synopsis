from dotenv import load_dotenv  # Import from python-dotenv
from pymongo import MongoClient
from PyPDF2 import PdfReader
import json
import os

load_dotenv()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_CONNECTION_URI")
client = MongoClient(MONGO_URI)
db = client["pdf_database"]  # Database name
collection = db["pdf_files"]  # Collection name

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

# Upload PDF to MongoDB
def upload_pdf_to_mongodb(uploaded_file):
    try:
        # Save the file as binary data in MongoDB
        file_data = {
            "filename": uploaded_file.name,
            "content": uploaded_file.getvalue()  # Using in-memory file content
        }
        collection.insert_one(file_data)
        print(f"File uploaded to MongoDB with filename: {uploaded_file.name}")
        return file_data["_id"]
    except Exception as e:
        print(f"Error uploading file to MongoDB: {e}")
        return None

# Retrieve a PDF from MongoDB (if needed)
def retrieve_pdf_from_mongodb(file_id):
    try:
        # Retrieve the file metadata from MongoDB using the file_id
        file_data = collection.find_one({"_id": file_id})
        if file_data:
            with open(file_data["filename"], "wb") as f:
                f.write(file_data["content"])
            print(f"File retrieved and saved as {file_data['filename']}")
        else:
            print("File not found in MongoDB.")
    except Exception as e:
        print(f"Error retrieving file from MongoDB: {e}")
