import json
import requests
import os
from core.utils import print_verbose

def seed_command(args):
    key = os.getenv("FORMBRICKS_API_KEY")
    if not key:
        print("FORMBRICKS_API_KEY missing in .env!")
        return

    base = "http://localhost:3000"
    headers = {"x-api-key": key, "Content-Type": "application/json"}

    # Get environmentId
    env_id = requests.get(f"{base}/api/v1/management/environments", headers=headers).json()["data"][0]["id"]
    print(f"Using environment: {env_id}")

    # Load data
    surveys = json.load(open("data/surveys.json"))
    users = json.load(open("data/users.json"))
    responses = json.load(open("data/responses.json"))

    # Replace placeholder
    for s in surveys:
        s["environmentId"] = env_id

    # Seed users (invites)
    for u in users:
        requests.post(f"{base}/api/v1/management/invites", headers=headers,
                      json={"email": u["email"], "role": u["role"]})
        print(f"Invited {u['email']} as {u['role']}")

    # Seed surveys
    survey_map = {}
    for s in surveys:
        r = requests.post(f"{base}/api/v1/management/surveys", headers=headers, json=s)
        sid = r.json().get("id")
        survey_map[s["name"]] = sid
        print(f"Created survey: {s['name']}")

    # Seed responses (client API - no key)
    for resp in responses:
        sid = survey_map.get(resp["surveyName"])
        if sid:
            body = {"surveyId": sid, "data": resp["data"], "finished": True}
            requests.post(f"{base}/api/v1/client/{env_id}/responses", json=body)
            print(f"Seeded response for {resp['surveyName']}")

    print("\nDONE! Check http://localhost:3000 → surveys + responses are there!")