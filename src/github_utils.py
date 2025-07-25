from github import Github
from git import Repo
from pathlib import Path
from .config import GITHUB_TOKEN
from .logger import logger

gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None
print(gh)

def clone_repo(repo_full_name, root_dir: Path):
    dest = root_dir / repo_full_name.replace("/", "_")
    if dest.exists():
        logger.info(f"Reusing existing clone: {repo_full_name}")
    else:
        logger.info(f"Cloning {repo_full_name}")
        try:
            Repo.clone_from(f"https://github.com/{repo_full_name}.git", dest)
        except Exception as e:
            logger.error(f"Failed to clone {repo_full_name}: {e}")
            return None
    return dest