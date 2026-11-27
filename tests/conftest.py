"""pytest 配置：把样品根目录加入 sys.path，使 tests 能 import src。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
