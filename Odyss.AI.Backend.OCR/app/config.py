import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    LOCAL_DOC_PATH = os.getenv("LOCAL_DOC_PATH")
    LOCAL_IMG_PATH = os.getenv("LOCAL_IMG_PATH")

