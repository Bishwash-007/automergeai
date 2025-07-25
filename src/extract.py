from git import Repo
from .logger import logger

def extract_merge_data(repo_path):
    logger.info(f"Extracting merge commits from repo: {repo_path.name}")
    repo = Repo(repo_path)
    data = []

    for commit in repo.iter_commits('--all'):
        if len(commit.parents) != 2:
            continue
        p1, p2 = commit.parents
        try:
            base = repo.git.merge_base(p1, p2)
        except Exception:
            logger.debug(f"Skipping commit {commit.hexsha}: no merge_base found")
            continue
        for diff in commit.diff(p1):
            file_path = diff.a_path or diff.b_path
            if not file_path:
                continue
            try:
                base_blob = repo.git.show(f"{base}:{file_path}")
                left_blob = repo.git.show(f"{p1.hexsha}:{file_path}")
                right_blob = repo.git.show(f"{p2.hexsha}:{file_path}")
                merged_blob = repo.git.show(f"{commit.hexsha}:{file_path}")
                data.append({
                    "base": base_blob,
                    "left": left_blob,
                    "right": right_blob,
                    "merged": merged_blob,
                    "file": file_path,
                    "repo": repo_path.name,
                    "commit": commit.hexsha
                })
                logger.debug(f"Commit {commit.hexsha}: added file {file_path}")
            except Exception:
                logger.warning(f"Skipping file {file_path} in commit {commit.hexsha}")

    logger.info(f"Found {len(data)} merge-resolved files in {repo_path.name}")
    return data