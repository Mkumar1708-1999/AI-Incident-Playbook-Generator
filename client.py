# email_summarizer_client.py
import requests

API_URL = "http://localhost:8001/summarize"

def get_summary(email_content):
    """
    Send a POST request to the API with the email content and return the summary
    if the request is successful. If the request fails, raise an exception.

    Args:
        email_content (str): The content of the email to summarize

    Returns:
        str: The summary of the email
    """
    response = requests.post(API_URL, json={"email_content": email_content})
    if response.status_code == 200:
        # Return the summary from the API response
        return response.json().get("summary")
    else:
        # Raise an exception if the request fails
        raise Exception(f"API Error: {response.status_code} - {response.text}")


# Example usage
if __name__ == "__main__":
    email_content = "Canadian law database CanLII sues Caseway AI over content scraping"
    summary = get_summary(email_content)
    print("Response\n:", summary)
