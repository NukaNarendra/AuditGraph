import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" Error: API Key not found in .env")
else:
    try:
        genai.configure(api_key=api_key)
        print(f" Key found: {api_key[:5]}... checking available models...\n")

        print("--- AVAILABLE MODELS ---")
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"• {m.name}")
                found = True

        if not found:
            print(
                " No content generation models found. Check if 'Generative Language API' is enabled in Google Cloud Console.")

    except Exception as e:
        print(f" Connection Error: {e}")