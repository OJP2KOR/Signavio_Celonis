# BPMN Cloud Upload Tool

This Streamlit application allows you to upload BPMN diagrams to the Celonis Process Repository. The tool provides a user-friendly interface to manage categories, process models, and tags before uploading your BPMN content.

## Features

- Upload BPMN XML files to Celonis Process Repository
- Browse and select from existing categories or create new ones
- Browse and select from existing process models or create new ones
- Add tags to your process models
- Support for corporate proxy configuration
- Interactive user interface with step-by-step workflow

## Prerequisites

- Python 3.7 or higher
- Celonis API key with appropriate permissions
- Access to Celonis Process Repository

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your credentials:
   - Rename the `credential.env.template` file to `credential.env`
   - Fill in your Celonis API key and proxy credentials in the `.env` file

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Access the application in your web browser (typically at http://localhost:8501).

3. Follow the step-by-step workflow in the application:
   - Configure credentials if not already set
   - Upload a BPMN file
   - Select or create a category
   - Select or create a process model
   - Add tags (optional)
   - Upload the BPMN content to Celonis

## Workflow Details

### 1. Configure Credentials
- Enter your Celonis API key
- Configure proxy settings if necessary

### 2. BPMN File
- Upload a BPMN XML file
- Future versions will support direct import from Signavio

### 3. Category Selection
- Browse the category hierarchy 
- Select an existing category or create a new one