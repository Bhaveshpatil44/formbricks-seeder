import os
import time
import subprocess
from pathlib import Path
from .utils import run_command, print_verbose

def up_command(args):
    verbose = args.verbose
    print_verbose("Starting up...", verbose)

    compose_file = Path("docker-compose.yml")
    env_file = Path(".env")

    if not compose_file.exists():
        print("Downloading docker-compose.yml ...")
        run_command("curl -o docker-compose.yml https://raw.githubusercontent.com/formbricks/formbricks/stable/docker/docker-compose.yml", verbose)

    if not env_file.exists():
        print("Downloading .env.example ...")
        run_command("curl -o .env https://raw.githubusercontent.com/formbricks/formbricks/stable/docker/.env.example", verbose)

    # Generate secrets
    secrets = ["NEXTAUTH_SECRET", "ENCRYPTION_KEY", "CRON_SECRET"]
    changed = False
    with open(".env", "r") as f:
        lines = f.readlines()
    with open(".env", "w") as f:
        for line in lines:
            for key in secrets:
                if line.startswith(key + "="):
                    if "your-secret-key" in line or line.strip().endswith("="):
                        new_secret = subprocess.check_output(
                            ["openssl", "rand", "-hex", "32"], text=True
                        ).strip()
                        line = f"{key}={new_secret}\n"
                        changed = True
            f.write(line)
    if changed:
        print("Generated random secrets")

    print("Starting Formbricks (1-2 minutes first time)...")
    run_command("docker compose up -d", verbose)

    print("Waiting for healthy", end="")
    for _ in range(40):
        time.sleep(3)
        try:
            result = subprocess.run(
                'curl -s http://localhost:3000/health',
                shell=True,
                capture_output=True,
                text=True
            )
            if "ok" in result.stdout.lower():
                print("\nHEALTHY!")
                break
        except:
            pass
        print(".", end="", flush=True)
    else:
        print("\nStill starting - ok, normal first time")

    print("\nFormbricks is running!")
    print("Open in browser: http://localhost:3000")
    print("Do the setup wizard → create user")
    print("Then Settings → API Keys → Create → copy the key")
    print("Paste it into .env file: FORMBRICKS_API_KEY=your_key_here")

def down_command(args):
    print("Stopping everything...")
    run_command("docker compose down -v")
    print("All clean!")