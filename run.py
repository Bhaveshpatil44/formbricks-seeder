import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyATnXNo5lAYTpewP0KhNlE_wf35c2Hiu4M")

# List available models
for m in genai.list_models():
    print(m.name)