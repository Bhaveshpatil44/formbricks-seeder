# core/utils.py

import json
import sys
import subprocess


def print_verbose(msg: str, verbose: bool = False):
    """Prints a message if verbose mode is enabled."""
    if verbose:
        print(f"[DEBUG] {msg}")


def run_command(cmd: str, cwd: str = None):
    """Run a shell command and display output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")
        return False


def load_json(file_path: str):
    """Loads JSON data from a file, expecting a list as the root object."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSON must be a list")
        return data

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)


def validate_survey(survey: dict) -> bool:
    """Validates if a dictionary contains minimum required survey fields."""
    required = ["name", "type", "status", "environmentId", "questions"]
    if not all(key in survey for key in required):
        return False

    if survey["type"] != "link" or survey["status"] != "draft":
        return False

    questions = survey.get("questions", [])
    if not isinstance(questions, list) or len(questions) < 2:
        return False

    q_types = [q.get("type") for q in questions]
    if "openText" not in q_types:
        return False
    if not any(q in ["multipleChoiceSingle", "nps"] for q in q_types):
        return False

    return True


def validate_user(user: dict) -> bool:
    """Validates if a user dictionary contains valid role and email."""
    return (
        "email" in user
        and "role" in user
        and user["role"] in ["manager", "owner"]
    )


def validate_response(resp: dict) -> bool:
    """Validates if a response dictionary has valid data structure."""
    if "data" not in resp or not isinstance(resp["data"], dict):
        return False
    if not resp.get("finished", False):
        return False
    return True


def check_docker():
    """Checks if Docker Compose is installed and accessible."""
    try:
        subprocess.run(
            ["docker", "compose", "version"],
            check=True,
            capture_output=True
        )
    except Exception:
        print("Docker Compose not installed or not in PATH.")
        sys.exit(1)