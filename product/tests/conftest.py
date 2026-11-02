import sys
from pathlib import Path

# Let the tests import app.py's neighbours (lookup.py and bot.py) directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
