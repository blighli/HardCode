import subprocess
import os

try:
    date_proc = subprocess.run(
        ["git", "log", "--format=%cd", "--date=format:%Y%m%d", "-1"],
        capture_output=True, text=True
    )
    date = date_proc.stdout.strip()

    count_proc = subprocess.run(
        ["git", "log", "--format=%cd", "--date=format:%Y%m%d"],
        capture_output=True, text=True
    )
    commits = count_proc.stdout.strip().split('\n')
    commit_count = sum(1 for c in commits if c == date)
    version = f"{date}.{commit_count}"
except Exception:
    version = "0.0.0"

with open(os.path.join("assets", "version"), "w") as f:
    f.write(version)