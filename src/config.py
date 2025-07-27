import os
from pathlib import Path

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
YOUR_REPOS = [
    "Bishwash-007/SubscriptionTracker"
]
REPOS_ROOT = Path("cloned_repos")
OUTPUT_CSV = "./data/SubscriptionTracker.csv"