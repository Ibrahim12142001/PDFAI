from django.conf import settings
import requests

# OpenAI credentials
api_endpoint = getattr(settings, 'OPENAI_API_ENDPOINT')
openai_api_key = getattr(settings, 'OPENAI_API_KEY')
model_name = "gpt-4-turbo"

# Define the path to the document file
document_file_path = "test.txt"

# Reads in txt document contents
def read_document(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        doc_content = file.read()
    return doc_content

# Creates prompt that has the context of a document's content
def add_doc_to_prompt(doc_content, input):
    # print("add_doc_to_prompt called")
    chat_input = "Read the following document:" + doc_content + "\n\n" + 'User: ' + input + '\n'
    return chat_input

# Uses OpenAI API to answer user prompts.
def chat_with_openai_api(conversation_input):
    headers = {
        "api-key": openai_api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "model":"gpt-4-turbo",
        "messages": conversation_input,
        "temperature": 0.2,
        "frequency_penalty":0,
        "presence_penalty":0,
        "stop": None
    }
    
    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        print("Token usage:", response_json["usage"]["total_tokens"])
        return response_json["choices"][0]["message"]["content"]
    else:
        print("Error: ", response.status_code)
        return None


