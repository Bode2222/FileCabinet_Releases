# scripts/refresh_tuf.py
from tufup.repo import Repository

def main():
    # Load the repo context (this handles key loading, thresholds, config) 
    repo = Repository.from_config()
    # Sign snapshot with threshold 
    repo.refresh_expiration_date("snapshot", 1) 
    repo.threshold_sign("snapshot", "./dist-keys/snapshot") 
    repo.refresh_expiration_date("timestamp", 1) 
    repo.threshold_sign("timestamp", "./dist-keys/timestamp_key") 
    print("Refreshed snapshot and timestamp")

if __name__ == "__main__":
    main()
