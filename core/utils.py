import subprocess
import sys

DOCKER_PATH = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"

def print_verbose(msg: str, verbose: bool = False):
    if verbose:
        print(f"[DEBUG] {msg}")

def run_command(cmd: str, verbose: bool = False):
    full_cmd = cmd.replace("docker", f'"{DOCKER_PATH}"')
    print_verbose(f"Running: {full_cmd}", verbose)
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed!\n{e.stderr}")
        sys.exit(1)

def check_docker():
    try:
        run_command("docker compose version", verbose=False)
    except:
        print("Docker is not running or path issue.")
        print("Please open Docker Desktop first!")
        sys.exit(1)