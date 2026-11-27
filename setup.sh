#!/usr/bin/env bash
# #2708 最小样品一键自测（setup.sh）
#
# 步骤：1/3 pytest；2/3 变异自证；3/3 MANIFEST 核验。
# 任何一步失败都退出非零。venv 建在仓内（家目录），不走 /tmp
# （/tmp 是小 tmpfs，空间不足）；pip 构建目录同样改到仓内 .tmp-pip。
set -u
cd "$(dirname "$0")"

CANDIDATES=".venv/bin/python python3.12 python3.11 python3 python"

exists() { [ -x "$1" ] || command -v "$1" >/dev/null 2>&1; }

pick_py() {
  for c in $CANDIDATES; do
    if exists "$c"; then
      if "$c" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
        echo "$c"
        return 0
      fi
    fi
  done
  return 1
}

pick_test_py() {
  for c in $CANDIDATES; do
    if exists "$c"; then
      if "$c" -c "import pytest" 2>/dev/null; then
        echo "$c"
        return 0
      fi
    fi
  done
  return 1
}

PY="$(pick_py)" || { echo "SELFTEST: FAIL (no Python >= 3.11)"; exit 1; }
TEST_PY="$(pick_test_py || true)"
if [ -z "$TEST_PY" ]; then
  echo "no interpreter with pytest; creating .venv and installing..."
  mkdir -p .tmp-pip
  export TMPDIR="$PWD/.tmp-pip"
  "$PY" -m venv .venv || { echo "SELFTEST: FAIL (venv create failed)"; exit 1; }
  .venv/bin/pip install -q --no-cache-dir -r requirements.txt || { echo "SELFTEST: FAIL (pip install failed)"; exit 1; }
  TEST_PY="$(pick_test_py || true)"
fi
[ -n "$TEST_PY" ] || { echo "SELFTEST: FAIL (no test interpreter with pytest)"; exit 1; }

echo "== 1/3 pytest =="
"$TEST_PY" -m pytest -q tests/ || { echo "SELFTEST: FAIL (pytest)"; exit 1; }

echo "== 2/3 mutation check =="
"$TEST_PY" scripts/mutation_check.py "$TEST_PY" || { echo "SELFTEST: FAIL (mutation check)"; exit 1; }

echo "== 3/3 MANIFEST check =="
[ -f MANIFEST ] || { echo "SELFTEST: FAIL (MANIFEST missing)"; exit 1; }
(cd "$(pwd)" && sha256sum -c MANIFEST) || { echo "SELFTEST: FAIL (MANIFEST mismatch)"; exit 1; }

echo "SELFTEST: PASS"
