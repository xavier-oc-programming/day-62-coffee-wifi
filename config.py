import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# Server
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-set-in-.env")
PORT = 5002
DEBUG = True

# Data
DATA_CSV = Path(__file__).parent / "cafe-data.csv"
CSV_HEADERS = ["Cafe Name", "Location", "Open", "Close", "Coffee", "Wifi", "Power"]

# Form choices
COFFEE_CHOICES = ["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
WIFI_CHOICES   = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
POWER_CHOICES  = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]
