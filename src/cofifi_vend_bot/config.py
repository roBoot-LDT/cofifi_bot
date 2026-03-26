import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID")) if os.getenv("OWNER_CHAT_ID") else None
