#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""变异自证：证明测试真能抓住回归，不是恒绿。

A 相：原样跑 pytest 全过。
B 相：依次注入 3 个变异（每次只改一处，跑完立即恢复并核对 SHA256）：
  M1 主题行改成超长（30 字），预期 test_subject_length_all 失败；
  M2 激活有效期 72 小时改成 48 小时，预期 test_activation_invite_states_72h_validity 失败；
  M3 员工开通通知改成明文密码，预期 test_staff_no_plaintext_password 失败。
任一相不符合预期即 exit 1；全部符合打印 MUTATION CHECK: PASS。
用法：python3 scripts/mutation_check.py [pytest解释器]
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "emails.py"

MUTANTS = [
    (
        "M1-subject-too-long",
        '"subject": "会员空间平台正式上线",',
        '"subject": "会员空间平台正式上线三大功能一次看清欢迎回来体验新功能",',
        ["tests/test_emails.py::test_subject_length_all"],
    ),
    (
        "M2-validity-72h-to-48h",
        "激活链接自发送起 72 小时内有效",
        "激活链接自发送起 48 小时内有效",
        ["tests/test_emails.py::test_activation_invite_states_72h_validity"],
    ),
    (
        "M3-plaintext-password",
        "请点击以下链接设置您的登录密码：{{set_password_url}}。",
        "您的初始密码是 TempPass-0000，请妥善保管。",
        ["tests/test_emails.py::test_staff_no_plaintext_password"],
    ),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(py: str, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [py, "-m", "pytest", "-q", *args],
        cwd=ROOT, capture_output=True, text=True, timeout=600,
    )


def main() -> int:
    py = sys.argv[1] if len(sys.argv) > 1 else sys.executable
    original = TARGET.read_text(encoding="utf-8")
    sha_before = sha(TARGET)

    a = run(py, ["tests/"])
    last = a.stdout.strip().splitlines()[-1] if a.stdout.strip() else ""
    print("A-phase:", last)
    if a.returncode != 0:
        print("MUTATION CHECK: FAIL (A phase did not pass)")
        print(a.stdout[-2000:], a.stderr[-2000:])
        return 1

    caught = 0
    for name, anchor, mutated, tests in MUTANTS:
        assert anchor in original, f"mutation anchor not found: {name}"
        TARGET.write_text(original.replace(anchor, mutated, 1), encoding="utf-8")
        try:
            b = run(py, tests)
            failed = b.returncode != 0
            print(f"{name}: targeted test {'FAILED as expected' if failed else 'PASSED (NOT CAUGHT)'}")
            if failed:
                caught += 1
        finally:
            TARGET.write_text(original, encoding="utf-8")
        if sha(TARGET) != sha_before:
            print(f"MUTATION CHECK: FAIL ({name} not restored)")
            return 1

    print(f"caught {caught}/{len(MUTANTS)} mutants")
    if caught != len(MUTANTS):
        print("MUTATION CHECK: FAIL (not all mutants caught)")
        return 1
    print("MUTATION CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
