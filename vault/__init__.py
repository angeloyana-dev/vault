import os

home_path = os.path.expanduser('~')
db_path = f"{home_path}/.vault_db"
master_key_path = f"{db_path}/master_key.txt"
credentials_db_path = f"{db_path}/credentials.db"
os.makedirs(db_path, exist_ok=True)