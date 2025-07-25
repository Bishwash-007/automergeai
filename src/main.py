import pandas as pd
from tqdm import tqdm
import concurrent.futures

from .config import YOUR_REPOS, REPOS_ROOT, OUTPUT_CSV
from .logger import logger
from .github_utils import clone_repo
from .extract import extract_merge_data

def main():
    logger.info("Starting workflow with custom repo list")
    REPOS_ROOT.mkdir(exist_ok=True)
    
    clone_paths = []
    for full_name in YOUR_REPOS:
        path = clone_repo(full_name, root_dir=REPOS_ROOT)
        if path:
            clone_paths.append(path)
    
    all_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(extract_merge_data, p): p for p in clone_paths}
        for fut in tqdm(concurrent.futures.as_completed(futures),
                        total=len(futures), desc="Extracting merges"):
            path = futures[fut]
            try:
                result = fut.result()
                all_data.extend(result)
            except Exception as e:
                logger.error(f"Error processing {path.name}: {e}")
    
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_CSV, index=False)
    logger.info(f"Saved {len(df)} records to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()