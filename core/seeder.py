# core/seeder.py (Final Robust Version)

import json
import requests
import os
from core.utils import print_verbose
from requests.exceptions import RequestException, JSONDecodeError

def seed_command(args):
    key = os.getenv("FORMBRICKS_API_KEY")
    
    # --- DEBUG BLOCK & INITIAL KEY CHECK ---
    if not key:
        print("ERROR: FORMBRICKS_API_KEY is missing in .env or failed to load!")
        return
    if len(key) < 20:
        print(f"ERROR: FORMBRICKS_API_KEY is too short ({len(key)} chars). Check .env.")
        return
    print(f"DEBUG: Using API Key starting with: {key[:10]}...")
    
    base = "http://localhost:3000"
    headers = {"x-api-key": key, "Content-Type": "application/json"}

    env_id = None
    
    # --- 1. GET ENVIRONMENT ID (CRITICAL AUTHENTICATION CHECK) ---
    try:
        r = requests.get(f"{base}/api/v1/management/environments", headers=headers)
        
        # Check for explicit API error codes (401, 403, 404)
        if r.status_code != 200:
            print(f"\nFATAL ERROR: Failed to fetch environment ID. Status Code: {r.status_code}")
            print(f"Response Text: {r.text[:200]}")
            if r.status_code == 404:
                print("\nReason: Resource Not Found (404).")
                print("ACTION: Log into http://localhost:3000 and ensure your API Key's user has an active Product/Environment created.")
            elif r.status_code in [401, 403]:
                print("\nReason: Authentication Failed or Forbidden (401/403).")
                print("ACTION: Ensure API Key has 'Manage' permissions for Project/Organization.")
            return

        # Attempt to parse JSON only after a successful status code
        data = r.json()
        env_id = data["data"][0]["id"]
        
    except JSONDecodeError:
        print(f"\nFATAL ERROR: Failed to parse JSON response. Status: {r.status_code}")
        print("Reason: The API Key is likely valid but the target user has NO PRODUCTS/ENVIRONMENTS set up in the Formbricks UI.")
        return
    except RequestException as e:
        print(f"An unexpected request error occurred: {e}")
        return
    
    print(f"Using environment: {env_id}")

    # ---------------------------
    # 2. SEEDING LOGIC
    # ---------------------------
    
    # Load data (Assumes manual cleanup was done)
    try:
        surveys = json.load(open("data/surveys.json"))
        users = json.load(open("data/users.json"))
        responses = json.load(open("data/responses.json"))
    except FileNotFoundError as e:
        print(f"ERROR: Data file missing. Did you run 'python main.py formbricks generate'? File: {e}")
        return

    # Replace placeholder
    for s in surveys:
        s["environmentId"] = env_id

    # Seed users (invites)
    print("\n--- Seeding Users (Invites) ---")
    for u in users:
        r = requests.post(f"{base}/api/v1/management/invites", headers=headers,
                         json={"email": u["email"], "role": u["role"]})
        if r.status_code == 201:
            print(f"Invited {u['email']} as {u['role']} (Success)")
        else:
            print(f"Failed to invite {u['email']}. Status: {r.status_code}. Response: {r.text[:50]}")


    # Seed surveys
    print("\n--- Seeding Surveys ---")
    survey_map = {}
    for s in surveys:
        r = requests.post(f"{base}/api/v1/management/surveys", headers=headers, json=s)
        if r.status_code == 201:
            sid = r.json().get("id")
            survey_map[s["name"]] = sid
            print(f"Created survey: {s['name']} (ID: {sid})")
        else:
            print(f"Failed to create survey {s['name']}. Status: {r.status_code}. Response: {r.text[:50]}")


    # Seed responses (client API)
    print("\n--- Seeding Responses ---")
    for resp in responses:
        sid = survey_map.get(resp["surveyName"])
        if sid:
            body = {"surveyId": sid, "data": resp["data"], "finished": True}
            r = requests.post(f"{base}/api/v1/client/{env_id}/responses", json=body)
            if r.status_code == 201:
                print(f"Seeded response for {resp['surveyName']} (Success)")
            else:
                print(f"Failed to seed response for {resp['surveyName']}. Status: {r.status_code}. Response: {r.text[:50]}")


    print("\n✅ DONE! Check http://localhost:3000 → users, surveys, and responses are visible!")# core/seeder.py (Final Robust Version)

import json
import requests
import os
from core.utils import print_verbose
from requests.exceptions import RequestException, JSONDecodeError

def seed_command(args):
    key = os.getenv("FORMBRICKS_API_KEY")
    
    # --- DEBUG BLOCK & INITIAL KEY CHECK ---
    if not key:
        print("ERROR: FORMBRICKS_API_KEY is missing in .env or failed to load!")
        return
    if len(key) < 20:
        print(f"ERROR: FORMBRICKS_API_KEY is too short ({len(key)} chars). Check .env.")
        return
    print(f"DEBUG: Using API Key starting with: {key[:10]}...")
    
    base = "http://localhost:3000"
    headers = {"x-api-key": key, "Content-Type": "application/json"}

    env_id = None
    
    # --- 1. GET ENVIRONMENT ID (CRITICAL AUTHENTICATION CHECK) ---
    try:
        r = requests.get(f"{base}/api/v1/management/environments", headers=headers)
        
        # Check for explicit API error codes (401, 403, 404)
        if r.status_code != 200:
            print(f"\nFATAL ERROR: Failed to fetch environment ID. Status Code: {r.status_code}")
            print(f"Response Text: {r.text[:200]}")
            if r.status_code == 404:
                print("\nReason: Resource Not Found (404).")
                print("ACTION: Log into http://localhost:3000 and ensure your API Key's user has an active Product/Environment created.")
            elif r.status_code in [401, 403]:
                print("\nReason: Authentication Failed or Forbidden (401/403).")
                print("ACTION: Ensure API Key has 'Manage' permissions for Project/Organization.")
            return

        # Attempt to parse JSON only after a successful status code
        data = r.json()
        env_id = data["data"][0]["id"]
        
    except JSONDecodeError:
        print(f"\nFATAL ERROR: Failed to parse JSON response. Status: {r.status_code}")
        print("Reason: The API Key is likely valid but the target user has NO PRODUCTS/ENVIRONMENTS set up in the Formbricks UI.")
        return
    except RequestException as e:
        print(f"An unexpected request error occurred: {e}")
        return
    
    print(f"Using environment: {env_id}")

    # ---------------------------
    # 2. SEEDING LOGIC
    # ---------------------------
    
    # Load data (Assumes manual cleanup was done)
    try:
        surveys = json.load(open("data/surveys.json"))
        users = json.load(open("data/users.json"))
        responses = json.load(open("data/responses.json"))
    except FileNotFoundError as e:
        print(f"ERROR: Data file missing. Did you run 'python main.py formbricks generate'? File: {e}")
        return

    # Replace placeholder
    for s in surveys:
        s["environmentId"] = env_id

    # Seed users (invites)
    print("\n--- Seeding Users (Invites) ---")
    for u in users:
        r = requests.post(f"{base}/api/v1/management/invites", headers=headers,
                         json={"email": u["email"], "role": u["role"]})
        if r.status_code == 201:
            print(f"Invited {u['email']} as {u['role']} (Success)")
        else:
            print(f"Failed to invite {u['email']}. Status: {r.status_code}. Response: {r.text[:50]}")


    # Seed surveys
    print("\n--- Seeding Surveys ---")
    survey_map = {}
    for s in surveys:
        r = requests.post(f"{base}/api/v1/management/surveys", headers=headers, json=s)
        if r.status_code == 201:
            sid = r.json().get("id")
            survey_map[s["name"]] = sid
            print(f"Created survey: {s['name']} (ID: {sid})")
        else:
            print(f"Failed to create survey {s['name']}. Status: {r.status_code}. Response: {r.text[:50]}")


    # Seed responses (client API)
    print("\n--- Seeding Responses ---")
    for resp in responses:
        sid = survey_map.get(resp["surveyName"])
        if sid:
            body = {"surveyId": sid, "data": resp["data"], "finished": True}
            r = requests.post(f"{base}/api/v1/client/{env_id}/responses", json=body)
            if r.status_code == 201:
                print(f"Seeded response for {resp['surveyName']} (Success)")
            else:
                print(f"Failed to seed response for {resp['surveyName']}. Status: {r.status_code}. Response: {r.text[:50]}")


    print("\n✅ DONE! Check http://localhost:3000 → users, surveys, and responses are visible!")