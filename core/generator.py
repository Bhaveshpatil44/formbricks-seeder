import json
import os
import google.generativeai as genai
from core.utils import print_verbose

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_command(args):
    verbose = args.verbose
    print_verbose("Starting data generation with Gemini...", verbose)
    os.makedirs("data", exist_ok=True)

    # 5 realistic surveys
    prompt_surveys = """
    Give me ONLY a valid JSON array of 5 different realistic surveys for Formbricks.
    Each survey must have:
    - name (realistic title)
    - type: "link"
    - status: "draft"
    - environmentId: "PLACEHOLDER"
    - questions: 3-5 questions mixing openText, multipleChoiceSingle, nps
    Return ONLY the JSON array, no explanation.
    """
    response = model.generate_content(prompt_surveys)
    surveys = json.loads(response.text.strip("`"))
    for s in surveys:
        s["environmentId"] = "PLACEHOLDER"
    with open("data/surveys.json", "w") as f:
        json.dump(surveys, f, indent=2)
    print("Generated 5 surveys → data/surveys.json")

    # 10 users
    prompt_users = "Give me ONLY valid JSON array of 10 objects: [{name: 'John Doe', email: 'john@company.com', role: 'manager' or 'owner'}]. Mix roles. Real names/emails."
    users = json.loads(model.generate_content(prompt_users).text.strip("`"))
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=2)
    print("Generated 10 users → data/users.json")

    # 1 response per survey
    responses = []
    for survey in surveys:
        prompt = f"Give me ONLY one valid Formbricks response JSON for this survey:\n{json.dumps(survey['questions'][:4])}\nInclude realistic answers and finished: true"
        resp_text = model.generate_content(prompt).text.strip("`")
        try:
            data = json.loads(resp_text)
            responses.append({"surveyName": survey["name"], "data": data.get("data", {}), "finished": True})
        except:
            responses.append({"surveyName": survey["name"], "data": {}, "finished": True})
    with open("data/responses.json", "w") as f:
        json.dump(responses, f, indent=2)
    print("Generated 5 responses → data/responses.json")
    print("All data ready! Run: python main.py formbricks seed")