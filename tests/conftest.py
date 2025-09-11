import sys
from pathlib import Path

# Ensure project root is on the import path for tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
