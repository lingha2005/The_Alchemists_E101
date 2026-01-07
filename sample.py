import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

print("Models that support generateContent:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
