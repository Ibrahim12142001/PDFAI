from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.shortcuts import render, redirect
import json
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from pypdf import PdfReader
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
from pdfminer.high_level import extract_text
from presidio_analyzer import AnalyzerEngine
import fitz  

def banner_image(request):
    image_path = os.path.join(settings.BASE_DIR, 'combined_openAI_app', 'banner.jpg')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def home(request):
    return render(request, 'home.html')

def PII(request):
    return render(request, 'PII.html')

def SSC(request):
    return render(request, 'SSC.html')

     
def chat_home(request):
    return render(request, 'chat_home.html')
    
def overview(request):
    return render(request, 'overview.html')

def calculate_sensitivity_score(analyzer_results):
    weights = {
        'PERSON': 0.05,
        'LOCATION': 0.05,
        'DATE_TIME': 0.02,
        'ORGANIZATION': 0.1,
        'PHONE_NUMBER': 0.3,
        'EMAIL_ADDRESS': 0.3,
        'CREDIT_CARD': 1.0,
        'NATIONAL_ID': 1.0,
    }
    score = sum(weights.get(result.entity_type, 0) * 100 for result in analyzer_results)  # Convert to percentage
    return min(score, 100)  # Ensure the score does not exceed 100%

# Function to perform PII recognition using Presidio
def pii_recognition_example(pdf_path):
    analyzer = AnalyzerEngine()

    # Extract text from PDF
    text = extract_text(pdf_path)

    # Analyze the text for PII using Presidio
    analyzer_results = analyzer.analyze(text=text, language='en')

    # Calculate sensitivity score
    sensitivity_score = calculate_sensitivity_score(analyzer_results)

    return sensitivity_score



# Function to perform the sensitivity analysis
def analyze_sensitivity(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        document_path = fs.path(filename)
        analyzer = AnalyzerEngine()

        # Extract text from PDF
        score = pii_recognition_example(document_path)

        # Clean up the file after analysis
        fs.delete(filename)

        print("Sensitivity Score Calculated: ", score)

        return JsonResponse({"score": score})



def upload_document2(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        if uploaded_file and uploaded_file.name.lower().endswith('.pdf'):
            fs = FileSystemStorage()
            
            # Split the filename and extension
            name, extension = os.path.splitext(uploaded_file.name)
            # Define the new filename with '-redacted' appended
            new_filename = f"{name}-redacted{extension}"
            
            # Save the original file
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            full_temp_path = os.path.join(fs.location, filename)
            
            # Define the output path with the new filename
            output_pdf_path = os.path.join(fs.location, new_filename)
            
            # Call your redaction function here
            redact_pdf_based_on_pii(full_temp_path, output_pdf_path)

            # Make sure to delete the original file
            os.remove(full_temp_path)
            
            # Return the path to the redacted PDF with the new filename
            redacted_pdf_url = fs.url(new_filename)
            return JsonResponse({'redactedPdfUrl': redacted_pdf_url})
        else:
            return HttpResponseBadRequest("Please upload a valid PDF file.")

 
 

 
 
def redact_pdf_based_on_pii(pdf_path, output_pdf_path):
    """
    Redacts specific PII types in a PDF file.
    
    :param pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path where the redacted PDF will be saved.
    """
    # Initialize Presidio Analyzer
    analyzer = AnalyzerEngine()

    # Define PII entities to redact
    entities_to_redact = [
        'PERSON', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 
        'CREDIT_CARD', 'IBAN', 'US_BANK_NUMBER', 
        'DATE_TIME', 'NATIONAL_ID', 'SSN'
    ]

    # Open the PDF
    doc = fitz.open(pdf_path)
    
    for page in doc:
        text = page.get_text("text")
        analyzer_results = analyzer.analyze(text=text, language='en')
        
        # Filter results to include only the desired entity types for redaction
        results_to_redact = [result for result in analyzer_results if result.entity_type in entities_to_redact]
        
        for result in results_to_redact:
            # Search for the text of each result to get the position for redaction
            spans = page.search_for(text[result.start:result.end])
            for span in spans:
                # Add redaction annotation
                page.add_redact_annot(span, fill=(0, 0, 0))  # Use black color to redact

        # Apply the redactions
        page.apply_redactions()

    # Save the redacted PDF
    doc.save(output_pdf_path, garbage=4, deflate=True)
    doc.close()

 

