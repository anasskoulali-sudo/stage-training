from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DEFAULT_DATABASE_URL = "mysql+pymysql://root@127.0.0.1:3306/stage_site"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
