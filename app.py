# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Initialize the FastAPI app
app = FastAPI()

# Define request and response schemas
class EmailSummaryRequest(BaseModel):
    email_content: str

class EmailSummaryResponse(BaseModel):
    summary: str

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/v1/completions"  # Default Ollama API URL

# Summarization endpoint
@app.post("/summarize", response_model=EmailSummaryResponse)
async def summarize_email(request: EmailSummaryRequest):
    """
    Endpoint to summarize an email's content using Ollama's API.

    Args:
        request (EmailSummaryRequest): Request object containing email content.

    Returns:
        EmailSummaryResponse: Response object containing the summary of the email.
    """
    try:
        # Prepare the prompt for Ollama API with the email content
        prompt = (
        "Generate a detailed AI incident response playbook using the following structure:\n"
        "1. Immediate Response\n"
        "2. Investigation\n"
        "3. Internal Communication\n"
        "4. External Communication\n"
        "5. Recovery and Mitigation\n" 
        f"{request.email_content}")

        # Define the payload for the POST request to Ollama's API
        payload = {
            "model": "IncidentLLM:latest",  # Specify the model name
            "prompt": prompt,
            "max_tokens": 1000  # Set the maximum tokens for the summary
        }

        # Send the POST request to Ollama's API
        response = requests.post(OLLAMA_API_URL, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the summary from the API response
            summary = response.json().get("choices", [{}])[0].get("text", "").strip()
            return EmailSummaryResponse(summary=summary)
        else:
            # Raise an HTTPException if the API call was unsuccessful
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        # Handle any exceptions that occur during the process
        raise HTTPException(status_code=500, detail=str(e))
