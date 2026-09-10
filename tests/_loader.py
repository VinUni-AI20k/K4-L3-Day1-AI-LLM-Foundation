"""
Nạp bài làm của sinh viên: ưu tiên solution/solution.py, fallback template.py.
Dùng chung cho cả 4 file test — import: from tests._loader import MOD
"""

import importlib.util
import sys
from pathlib import Path

DAY_DIR = Path(__file__).parent.parent
SOLUTION_DIR = DAY_DIR / "solution"


def _load(path: Path, unique_name: str):
    if unique_name in sys.modules:
        return sys.modules[unique_name]
    spec = importlib.util.spec_from_file_location(unique_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = mod
    spec.loader.exec_module(mod)
    return mod


if (SOLUTION_DIR / "solution.py").exists():
    MOD = _load(SOLUTION_DIR / "solution.py", "k4_day01_solution")
else:
    MOD = _load(DAY_DIR / "template.py", "k4_day01_template")
