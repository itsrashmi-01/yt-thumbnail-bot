from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID") or 0)
    API_HASH = os.getenv("API_HASH")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "ytthumbbot")
    FORCE_CHANNEL = os.getenv("FORCE_CHANNEL")  # @channel or -100...
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL") or 0)
    START_PIC = os.getenv("START_PIC")
    BOT_NAME = os.getenv("BOT_NAME", "YTThumbBot")
    OWNER_ID = int(os.getenv("OWNER_ID") or 0)
