import os
from dotenv import load_dotenv

load_dotenv()
username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_HOSTNAME")
database = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT", 3306)  #  to 3306 if not specified


class Config:
    SECRET_KEY = os.getenv("SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
    )
