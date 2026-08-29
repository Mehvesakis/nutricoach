import google.generativeai as genai

# API anahtarını buraya yapıştır
import os
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

print("Senin API anahtarına tanımlı kullanılabilir modeller:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)