from git import Repo

def clone_repo(repo_full_name, root_dir, logger):
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

def try_git_show(repo, blob_ref):
    try:
        return repo.git.show(blob_ref)
    except Exception:
        return ""