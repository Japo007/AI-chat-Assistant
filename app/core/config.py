import os
from dotenv import load_dotenv

load_dotenv()

PDL_API_KEY = os.getenv("PDL_API_KEY")
PDL_BASE_URL = "https://api.peopledatalabs.com/v5"