from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
INPUT_CSV = BASE_DIR / "input" / "cafe-data.csv"
DATA_CSV = BASE_DIR / "data" / "cafe-data.csv"

# Server
PORT = 5003

# Form choices
COFFEE_CHOICES = ["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
WIFI_CHOICES = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
POWER_CHOICES = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

# CSV
CSV_HEADERS = ["Cafe Name", "Location", "Open", "Close", "Coffee", "Wifi", "Power"]
