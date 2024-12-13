# AI Tools Suite Web Application

A web application built with Django, Python, CSS, HTML, and JavaScript, offering a suite of AI-powered tools for document analysis, sensitivity scoring, and redaction.

---

## Features

### 1. **AI ChatBot**
   - Enables users to chat with their PDF document in real-time.
   - Suitable for general inquiries and simple prompts.
   - Side-by-side view of the AI chat and the document.
   - Highlights relevant pages where answers are found for user verification.

### 2. **CSV/PDF Analyser**
   - Analyze and extract information from a PDF document.
   - Upload a PDF document alongside a CSV file containing engineered prompts for detailed analysis.

### 3. **Sensitivity Score Calculator**
   - Calculate the sensitivity of an uploaded document based on custom parameters.

### 4. **Redactor**
   - Scan and redact specific information from uploaded PDFs.
   - Utilizes **Presidio** for redaction capabilities.

---

## Tech Stack

- **Backend:** Django, Python
- **Frontend:** CSS, HTML, JavaScript
- **AI Integration:** OpenAI, Document Intelligence (OCR)
- **File Storage:** Azure Blob Storage
- **Redaction:** Presidio

---

## Setup and Installation

### Prerequisites
### 1. **Python installed on your system.**
### 2. **Clone this repository:**
   ```
   git clone https://github.com/your-repo-link.git
   ```

### 3. Environment Variables
   - Create a .env file in the project root directory.
   - Copy the contents of .env.example into .env.
   - Fill in the required API keys and endpoints:
   ```
   OPENAI_API_KEY = "your_openai_api_key"
   OPENAI_API_ENDPOINT = "your_openai_api_endpoint"
   
   BLOB_CONNECTION_STR = "your_blob_connection_string"
   BLOB_CONTAINER_NAME = "your_blob_container_name"
   
   openai.api_type = "your_openai_api_type"
   OPENAI_API_BASE = "your_openai_api_base"
   
   DI_API_ENDPOINT = "your_document_intelligence_api_endpoint"
   DI_API_KEY = "your_document_intelligence_api_key"
   ```
## Installation 

### 1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
### 2. Apply database migrations:
   ```
   python manage.py migrate
   ```
### 3. Start the development server
   ```
   python manage.py runserver
   ```

## Accessing the Application

### Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```
## Example Workflow

### 1. **AI ChatBot**
   - Ask questions in the chat interface.
   - View relevant document pages highlighted for easy answer verification.

### 2. **CSV/PDF Analyser**
   - Upload a PDF and a CSV file to extract meaningful insights.

### 3. **Sensitivity Score Calculator**
   - Get a sensitivity score based on defined criteria.

### 4. **Redactor**
   - Automatically redact sensitive information in uploaded documents.

## Technologies Used

| Technology | Purpose |
| -------- | ------- |
| Django & Python	| Backend and server logic | 
| CSS & HTML & JavaScript | Frontend styling and interactivity |
| OpenAI | Natural Language Processing (NLP) |
| Azure Blob Storage	| File storage and management |
| Document Intelligence | Optical Character Recognition (OCR) |
| Presidio | Redaction and sensitive data handling |

