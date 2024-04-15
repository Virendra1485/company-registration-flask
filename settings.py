"""Set Flask configuration from .env file."""
import os
from dotenv import load_dotenv

load_dotenv()

# General Config
SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")

# Database Config
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("DATABASE_HOST")
PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# SQLALCHEMY_DATABASE_URI = f"mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"


SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATA_SAMPLE_PATH = "".join(os.path.abspath(os.path.dirname(__file__) + "/data_sample"))





