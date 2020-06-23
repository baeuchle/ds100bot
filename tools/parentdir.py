"""Add parent directory to sys.path for module importing"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
