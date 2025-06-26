# tests/conftest.py
from pathlib import Path
from dotenv import load_dotenv

# repo_root/.env  ← assumes tests/ is one level inside the repo
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
