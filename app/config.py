import json
from pathlib import Path
from typing import Optional

Base_dir = Path(__file__).resolve().parent.parent

def get_secret(
        key: str,
        default_value: Optional[str] = None,
        json_path: str = str(Base_dir / "secrets.json")
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")
    
Mongo_DB_Name = get_secret("Mongo_DB_Name")
Mongo_Url = get_secret("Mongo_Url")
Naver_Api_Id = get_secret("Naver_Api_Id")
Naver_Api_Secret = get_secret("Naver_Api_Secret")

