from git import Repo
from .git_utils import try_git_show
from .diff_utils import get_diff

def extract_merge_data(repo_path, logger):
    logger.info(f"Extracting merge diffs from repo: {repo_path.name}")
    repo = Repo(repo_path)
    data = []

    for commit in repo.iter_commits('--all'):
        if len(commit.parents) != 2:
            continue

        p1, p2 = commit.parents
        try:
            base_commit = repo.git.merge_base(p1, p2)
        except Exception:
            logger.debug(f"Skipping commit {commit.hexsha}: no merge_base found")
            continue

        try:
            diffs = commit.diff(p1)
        except Exception as e:
            logger.warning(f"Failed to diff {commit.hexsha} vs parent: {e}")
            continue

        for diff in diffs:
            file_path = diff.a_path or diff.b_path
            if not file_path or diff.new_file or diff.deleted_file:
                continue

            try:
                base_blob = try_git_show(repo, f"{base_commit}:{file_path}")
                left_blob = try_git_show(repo, f"{p1.hexsha}:{file_path}")
                right_blob = try_git_show(repo, f"{p2.hexsha}:{file_path}")
                merged_blob = try_git_show(repo, f"{commit.hexsha}:{file_path}")

                left_diff = get_diff(base_blob, left_blob)
                right_diff = get_diff(base_blob, right_blob)
                merged_diff = get_diff(base_blob, merged_blob)

                if any([left_diff, right_diff, merged_diff]):
                    data.append({
                        "repo": repo_path.name,
                        "commit": commit.hexsha,
                        "commit_msg": commit.message.strip().replace('\n', ' '),
                        "file": file_path,
                        "left_diff": left_diff.strip(),
                        "right_diff": right_diff.strip(),
                        "merged_diff": merged_diff.strip()
                    })
                    logger.debug(f"Captured diff for {file_path} from commit {commit.hexsha}")
            except Exception as e:
                logger.warning(f"Skipping file {file_path} at {commit.hexsha}: {e}")
    return data