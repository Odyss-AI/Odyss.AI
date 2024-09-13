import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    LOCAL_DOC_PATH = os.getenv("LOCAL_DOC_PATH")
    TEI_URL = os.getenv("TEI_URL")
