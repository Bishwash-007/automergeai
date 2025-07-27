import concurrent.futures
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from config import GITHUB_TOKEN, YOUR_REPOS, REPOS_ROOT, OUTPUT_CSV
from logger import setup_logger
from git_utils import clone_repo
from extractor import extract_merge_data

from github import Github

def main():
    logger = setup_logger()
    gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None
    print(gh)

    logger.info("Starting workflow with custom repo list")
    REPOS_ROOT.mkdir(exist_ok=True)

    clone_paths = []
    for full_name in YOUR_REPOS:
        path = clone_repo(full_name, REPOS_ROOT, logger)
        if path:
            clone_paths.append(path)

    all_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(extract_merge_data, p, logger): p for p in clone_paths}
        for fut in tqdm(concurrent.futures.as_completed(futures),
                        total=len(futures), desc="Extracting merges"):
            path = futures[fut]
            try:
                result = fut.result()
                all_data.extend(result)
            except Exception as e:
                logger.error(f"Error processing {path.name}: {e}")

    Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(all_data, columns=["repo", "commit", "commit_msg", "file", "left_diff", "right_diff", "merged_diff"])
    df.to_csv(OUTPUT_CSV, index=False)
    logger.info(f"Saved {len(df)} records to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()