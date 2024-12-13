from django.db import models
import csv
from pypdf import PdfReader
import time
from demo.scripts.openai import chat_with_openai_api
import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from io import BytesIO
from django.conf import settings

endpoint = "https://pssidfodocumentintelligence.cognitiveservices.azure.com/" 
key = "39cb31f842ce4e92a6d0d7b33a5eda18" 

# Create your models here.
#------------------OpenAI Inputs--------------------
# Purpose: Stores document information related to usage of openAI
# Input: Document Information
# Output: Response data from asking openAI questions
# #----------------------------------------------------
# Class defining a Header value, usually taken from a csv file
class Header:
    def __init__(self, header_name, prompt):
        self._name = header_name
        self._prompt = prompt

    '''
    Creating a prompt based on a header name
    Return Value:
        - prompt (str): The generated prompt string.
    '''
    def create_prompt(self):
        return "For the given document, tell me the " + self._name + "using 4 or less words"

    '''
    Adding document content to the header's current prompt
    Parameters:
        - doc_content (str): The content of the document to be added to the prompt.
    '''
    def add_doc_content_to_prompt(self, doc_content):
        self._prompt = "Read the following document:" + doc_content + '\n\n' + 'User: ' + self._prompt + '\n'

    @property
    def name(self):
        return self._name

    @property
    def prompt(self):
        return self._prompt

class DocumentType:
    def __init__(self, name, file_path):
        self._name = name
        self._file_path = file_path
        self._col_prompts = self.extract_col_prompts()

    """
    Extract and create Header objects from a CSV file.

   Opens the specified CSV file, reads its content, and extracts pairs of column headers and prompts.
   Each pair is used to create a Header object, and a list of Header objects is returned.

   Return Value:
       - header_list (list of Header): A list of Header objects containing extracted column headers and prompts.
   """
    def extract_col_prompts(self):
        with open(self._file_path, encoding='cp1252') as file:
            reader = csv.reader(file)
            columns = list(reader)
        header_list = []
        for pair in columns:
            header_list.append(Header(pair[0], pair[1]))
        return header_list

    @property
    def col_prompts(self):
        return self._col_prompts

# Python object which holds information about a document
class Document:
    def __init__(self, file, doc_type: DocumentType):
        self._file_name = file.name
        self._content, self._refined_content = self.get_content(file)  
        self._type = doc_type
        self._openai_answers = {}

    '''
    Purpose: Extract the filename from the given file path and return it as a string.
    Parameters:
      - path (str): The complete file path from which the filename is to be extracted.
    Return Value:
      - file_name (str): The extracted filename as a string.
    '''
    def get_file_name(self, path):
        file_name = path.split("/")[-1]
        return file_name


    def refine_content(self, result):
        refined_data = {
            "Paragraphs": [
                {
                    "Content": paragraph.content,
                    "PageNumber": paragraph.bounding_regions[0].page_number if paragraph.bounding_regions else "N/A"
                } 
                for paragraph in result.paragraphs
            ],
            "Tables": [
                {
                    "RowCount": table.row_count,
                    "ColumnCount": table.column_count,
                    "Cells": [{"Content": cell.content} for cell in table.cells]
                } 
                for table in result.tables
            ]
        }

        refined_json = json.dumps(refined_data, indent=4)
        
        print(refined_json)
        
        return refined_json


    '''
    Read the content of a text document located at the specified path and return it as a string.
    Parameters:
      - path (str): File path to the text document that needs to be read.
    Return Value:
      - doc_content (str): Content of the file as a string
    '''
        
    def get_content(self, file):
        content = ""
        refined_content = "{}"  
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        file_name = file.name if file.name.lower().endswith('.pdf') else f"{f.name}.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, 'documents', file_name)

        try:
            with open(file_path, 'rb') as f:
                poller = client.begin_analyze_document("prebuilt-document", document=f)
                result = poller.result()

                content = result.content
                refined_content = self.refine_content(result)
        except Exception as e:
            print(f"Error processing document: {e}")

        return content, refined_content


    '''
    Obtain responses from OpenAI based on conversation headers and return them in a dictionary.
    Return Value:
        - _openai_answers (dict): A dictionary containing OpenAI responses, where header names serve as keys and 
        corresponding conversation responses as values. Each response is stored under the 'content' key of a 
        conversation item in a list. 
    '''
    def get_openai_responses(self):
        content = """ You are an AI assistant that reads in a document and answers user questions related to it. The 
        document is provided here:
        ---
        DOCUMENT
        """ + self._refined_content + """
        ---
        SPECIFICATIONS
        Only use information found in the document to answer questions. If you cannot find the information being 
        prompted to answer, respond with NA. When specified to return a list, separate list elements using “,” as
        a delimiter. If “Fisheries and Oceans Canada” is part of your response, condense to “DFO”. For each prompt,
        return exactly what is asked. DO NOT output extra unnecessary words. 
        IF an output structure is specified, follow that structure EXACTLY.
        In a single responce respond to each given user input sequencially, you will answer all these questions separated by 'A:'.
        At the end of each response add a source, like where you found the information. 
        Format it like this "Source: <The Document Title>, Page: <page number>, 
        Paragraph Number: <paragraph number> (the ith entry in "paragraphs": [] starting at 1), 
        Section Heading: <section heading>".
        """
        # Alternative prompt method, critical for GPT4 instead of GPT4 turbo
        # You will receive 7 or 8 tasks, in a single response, you will answer all these questions separated by 'A:'.

        conversation = [{'role': "system", "content": content}]
        for header in self._type.col_prompts:
            conversation.append({'role': 'user', 'content': header.prompt})
        response = chat_with_openai_api(conversation)

        # Separate response into individual responses
        response_sliced = response.split('A:')
        response_sliced = [part.strip() for part in response_sliced if part.strip()]
        i = 0
        for header in self._type.col_prompts:
            self._openai_answers[header.name] = response_sliced[i]
            i += 1
        #TODO: replace 15 second timeout with dynamic wait
        time.sleep(15)
        return self._openai_answers

    @property
    def file_name(self):
        return self._file_name


