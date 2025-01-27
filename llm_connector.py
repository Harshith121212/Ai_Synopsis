from langchain_groq import ChatGroq
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM connector
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=os.getenv("GROQ_LLM_MODEL"))

def llm_connection_helper (noOfLine):
    # Load the JSON file
    with open("preprocessed.json", "r") as file:
        json_content = json.load(file)

    # Convert JSON content to string
    json_str = json.dumps(json_content)

    # Ask the model to summarize the JSON content
    prompt = f"Here's a JSON file content: {json_str}. Can you summarize it, response should be within {noOfLine} points, ensure that in response do not use JSON word, instead of JSON use PDF"
    response = llm.invoke(prompt)
    return response.content


#llm_connection_helper()