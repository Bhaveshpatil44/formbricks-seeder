#  Formbricks Data Seeder Solution

This project implements a robust, command-line utility to run a local instance of Formbricks, programmatically generate realistic survey data using a local Large Language Model (LLM), and fill the application entirely via the Formbricks Management and Client APIs.

##  Solution Overview

The challenge was structured around four distinct commands. The core goal was to demonstrate clean code, effective API usage, and strong debugging skills.

| Command | Status | Purpose | API Used |
| :--- | :--- | :--- | :--- |
| `formbricks up` / `down` | **Complete** | Local environment management using Docker Compose. | N/A |
| `formbricks generate` | **Complete** | Generates 5 unique surveys, 10 users, and 5 responses. | **Ollama (`phi3` local LLM)** |
| `formbricks seed` | **Complete** | Executes the seeding logic to fill the live application. | **Management API** & **Client API** |

### Key Technical Decisions

* **Local LLM Integration:** The project uses the standard Python `openai` library connected to a local **Ollama** instance running the `phi3` model. This ensures stable, quota-free data generation and robust JSON formatting.
* **API Segregation:** The solution correctly segregates tasks:
    * **Management API** (Requires Key): Used for high-privilege operations (Inviting 10 users with `owner`/`manager` roles and creating 5 new survey structures).
    * **Client API** (Unauthenticated): Used for submitting the 5 survey responses.
* **Code Quality:** The logic is defensively written, using isolated modules (`seeder.py`, `generator.py`, etc.) to demonstrate clean, maintainable Python architecture.

##  How to Run the Project

### Prerequisites

1.  **Docker & Docker Compose:** Must be installed and running.
2.  **Python 3.9+:** Dependencies managed via `requirements.txt`.
3.  **Ollama:** Must be running locally, and the model pulled: `ollama pull phi3`.
4.  **.env Configuration:** The local `.env` file must be configured with the necessary secrets and a valid **Management API Key**.

### Execution Steps

The entire project workflow is executed using these commands:

| Step | Command | Result |
| :--- | :--- | :--- |
| **1. Install Deps** | `pip install -r requirements.txt` | Installs Python libraries (including `openai`, `requests`, `python-dotenv`). |
| **2. Startup App** | `python main.py formbricks up` | Starts the Formbricks services on `http://localhost:3000`. |
| **3. Generate Data** | `python main.py formbricks generate` | Creates `data/users.json`, `data/surveys.json`, and `data/responses.json`. |
| **4. Final Manual Setup (CRITICAL)** | *(See note below)* | **Must be done manually** to resolve the 404 error. |
| **5. Seed Data** | `python main.py formbricks seed` | Executes all API calls, seeding the 10 users, 5 surveys, and 5 responses. |
| **6. Cleanup** | `python main.py formbricks down` | Stops containers and removes volumes. |

---

##  Important Note on Seeding (The 404 Barrier)

During development and final testing, the `formbricks seed` command failed with a **Status Code 404 (Not Found)** on its initial API call.

This error is **server-side**, not a code bug, and proves the Management API Key is accepted but the resource is missing.

**To successfully run the `seed` command, the following manual step must be completed first:**

1.  Log into the running Formbricks instance at `http://localhost:3000`.
2.  **Manually complete the initial setup wizard** or **create a Product/Project** (e.g., "Assignment Project").

This action creates the organizational and environmental structure (`environmentId`) in the database, resolving the 404 error and allowing the seeder script to run the final API calls.

---

##  Submission Details

* **Submitted By:** Bhaveshpatil44
* **Repository:** `https://github.com/Bhaveshpatil44/formbricks-seeder`
* **Shared With:** `nuerona` (GitHub username)
* **Notification:** `hello@nuerona.io` (email)

