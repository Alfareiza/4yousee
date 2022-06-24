from pathlib import Path

from decouple import config

from fouryousee import FouryouseeAPI

TOKEN = config('TOKEN')
client = FouryouseeAPI(TOKEN)
BASE_DIR = Path(__file__).resolve().parent.parent
