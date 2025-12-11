

import json
import os
import openai
from core.utils import print_verbose

#  Ollama 
client = openai.OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama' 
) 
MODEL_NAME = "phi3"
JSON_FORMAT = {"type": "json_object"}

def generate_content_and_parse(prompt, label):
    """Handles LLM interaction and robust JSON parsing."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
               messages=[{"role": "user", "content": prompt}],
            response_format=JSON_FORMAT, 
            temperature=0.7
        )
        raw_text = response.choices[0].message.content
        return json.loads(raw_text), raw_text
    except Exception as e:
        print(f"ERROR: Failed to generate {label} data. Error: {e}")
        return None, None

def generate_command(args):
    print_verbose("Starting data generation with Ollama...", args.verbose)
    os.makedirs("data", exist_ok=True)
    surveys = [] 

    # 1. GENERATE SURVEYS
    prompt_surveys = "Give me ONLY a valid JSON array of 5 different realistic surveys. Each survey must have: name, type: 'link', status: 'draft', environmentId: 'PLACEHOLDER', and 3-5 questions mixing types: openText, multipleChoiceSingle, and nps. The response MUST be ONLY the JSON array."
    data, raw_text = generate_content_and_parse(prompt_surveys, "surveys")
    
    if data is None: return

    surveys = data.get('surveys', data) if isinstance(data, dict) else data
    if not isinstance(surveys, list): return
    
    for s in surveys:
        s["environmentId"] = "PLACEHOLDER"
            
    with open("data/surveys.json", "w") as f:
        json.dump(surveys, f, indent=2)
            
    print(f"Generated {len(surveys)} surveys → data/surveys.json")

    # 2. GENERATE USERS
    prompt_users = "Give me ONLY a valid JSON array of 10 objects. Each object must contain: {name, email, role: 'manager' or 'owner'}. Mix roles and use realistic names/emails."
    data, raw_text = generate_content_and_parse(prompt_users, "users")
    
    if data is None: return
    
    users = data.get('employees', data) if isinstance(data, dict) else data
    if not isinstance(users, list): return
    
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=2)
            
    print(f"Generated {len(users)} users → data/users.json")

    # 3. GENERATE RESPONSES
    responses = []
    print("Generating 1 response for each survey...")
    
    for survey in surveys:
        prompt = f"Generate ONLY one valid JSON object representing the Formbricks response DATA for this survey. Survey Questions: {json.dumps(survey.get('questions', [])[:4])}. The object MUST contain realistic answers for each question."
        
        data, raw_text = generate_content_and_parse(prompt, f"response for {survey.get('name', 'Unknown')}")

        if data is not None:
            responses.append({"surveyName": survey.get("name", "Unknown"), "data": data, "finished": True})
        else:
            responses.append({"surveyName": survey.get("name", "Unknown"), "data": {}, "finished": True})
            
    with open("data/responses.json", "w") as f:
        json.dump(responses, f, indent=2)
        
    print(f"Generated {len(responses)} responses → data/responses.json")
    print("\n✅ All data ready! Run: python main.py formbricks seed")