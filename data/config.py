import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = str(os.getenv("BOT_TOKEN"))
API_HASH = str(os.getenv("API_HASH"))
API_ID = int(os.getenv("API_ID"))

ADMINS = [5759932615] #5548351085 - Якудза
