import os
from pathlib import Path

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

YOUR_REPOS = [
    "remix-run/react-router"
    # Add your own "owner/repo" strings here
]

REPOS_ROOT = Path("cloned_repos")
OUTPUT_CSV = "./data/react_router.csv"