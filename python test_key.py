import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

response = model.generate_content("Test: Tagalog A1 單字")
print(response.text)

models = genai.list_models()
print([m.name for m in models if 'gemini' in m.name.lower()])
