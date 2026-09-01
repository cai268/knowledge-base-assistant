# tests/conftest.py
import sys
from pathlib import Path

root = Path(__file__).parent.parent
root_str = str(root)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

print(f"项目根目录: {root}")