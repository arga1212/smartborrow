# ai_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ambil API key dari .env
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str, model: str = "gemini-2.5-flash"):
    """
    Prompt -> response text
    """
    model_obj = genai.GenerativeModel(model)
    resp = model_obj.generate_content(prompt)
    return resp.text if hasattr(resp, "text") else str(resp)
