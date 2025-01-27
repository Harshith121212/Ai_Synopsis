from flask.cli import load_dotenv
from pymongo import MongoClient
from PyPDF2 import PdfReader
import bson
import json
import os
import gridfs


load_dotenv()
# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_CONNECTION_URI")
client = MongoClient(MONGO_URI)
db = client["pdf_database"]  # Database name
collection = db["pdf_files"]  # Collection name
fs = gridfs.GridFS(db)
# file_path = "sample.pdf"

def upload_pdf_to_mongodb(uploaded_file):
    try:
        # Save the file to GridFS
        file_id = fs.put(uploaded_file, filename=uploaded_file.name)
        print(f"File uploaded to MongoDB with GridFS ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file to MongoDB: {e}")
        return None
# extract text from pdf
def retrieve_pdf_from_mongodb(file_id):
    try:
        # Retrieve the file from GridFS using the file_id
        file_data = fs.get(file_id)
        with open(file_data.filename, "wb") as f:
            f.write(file_data.read())
        print(f"File retrieved and saved as {file_data.filename}")
    except Exception as e:
        print(f"Error retrieving file from MongoDB: {e}")

def extract_text_from_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

#save the extracted text to a json file

def save_text_to_json(extracted_text, output_file="preprocessed.json"):
    json_data = {"content": extracted_text}
    with open(output_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Extracted text saved to {output_file}")
    return output_file

#upload the extracted file to MongoDB

# def upload_pdf_to_mongodb(output_file):
#     with open(output_file, "rb") as file:
#         file_data = {
#             "filename": output_file.split("/")[-1],
#             "data": bson.Binary(file.read())  # Store binary data
#         }
#         file_id = collection.insert_one(file_data).inserted_id
#     print(f"File uploaded to MongoDB with ID: {file_id}")
#     return file_id


