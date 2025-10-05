# scripts/refresh_snapshot_timestamp.py
import os, tempfile, json
from tufup.repo import Repository

def _write_key(tmpdir, name, json_str):
    p = os.path.join(tmpdir, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(json_str)
    os.chmod(p, 0o600)
    return p

def main():
    # Prefer config; fall back to explicit paths
    try:
        repo = Repository.from_config()
    except FileNotFoundError:
        repo = Repository(app_name="app", repo_dir="dist-repo", keys_dir="dist-keys")

    # Write keys coming from env (GitHub Secrets)
    with tempfile.TemporaryDirectory() as tmp:
        snapshot_key_path = _write_key(tmp, "snapshot_key.json", os.environ["SNAPSHOT_KEY_JSON"])
        timestamp_key_path = _write_key(tmp, "timestamp_key.json", os.environ["TIMESTAMP_KEY_JSON"])

        # Refresh expirations then sign (your original flow)
        repo.refresh_expiration_date("snapshot", 1)
        repo.threshold_sign("snapshot", snapshot_key_path)
        repo.refresh_expiration_date("timestamp", 1)
        repo.threshold_sign("timestamp", timestamp_key_path)

    print("Refreshed snapshot and timestamp")

if __name__ == "__main__":
    main()
