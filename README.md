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
1. Python installed on your system.
2. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-link.git

