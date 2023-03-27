import re
import os.path
from pathlib import Path

ROOT_DIR = Path(__file__).parents[1].resolve()

text = open(ROOT_DIR / "README.md", "r", encoding="utf8").read()
demoji_test = re.sub(r':[\w\\]*:', '', text)

open(ROOT_DIR / "docs/README_pypi.md", "w", encoding="utf8").write(demoji_test)

print("Created PyPi-friendly README.md")