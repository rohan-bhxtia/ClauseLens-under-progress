import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("gemini_api_key"))

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="What is an LLM? Explain in two sentences."
)

print(response.text)
