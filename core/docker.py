

import os
import subprocess
from core.utils import run_command

COMPOSE_FILE = "docker-compose.yml"

def up_command(args):
    """Starts Formbricks using Docker Compose in detached mode."""
    if not os.getenv("WEBAPP_URL") or not os.getenv("NEXTAUTH_SECRET"):
        print("ERROR: Required environment variables are missing in .env.")
        return False

    print("Starting Formbricks services...")
    cmd = f"docker compose -f {COMPOSE_FILE} up -d"
    
    if run_command(cmd):
        print("\n✅ Formbricks is now running on http://localhost:3000.")
        return True
    return False


def down_command(args):
    """Stops and removes Formbricks services and their volumes."""
    print("Stopping and cleaning up Formbricks services...")
    cmd = f"docker compose -f {COMPOSE_FILE} down --volumes"
    
    if run_command(cmd):
        print("\n✅ Formbricks services and volumes have been cleaned up.")
        return True
    return False