import google.generativeai as genai

# API anahtarını buraya yapıştır
genai.configure(api_key="API_ANAHTARI_BURAYA_GELECEK")

print("Senin API anahtarına tanımlı kullanılabilir modeller:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)