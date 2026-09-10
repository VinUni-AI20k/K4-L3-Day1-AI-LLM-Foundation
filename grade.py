#!/usr/bin/env python3
"""
Chấm điểm tự động — K4 Ngày 1: Khám Phá LLM API

Cách dùng (chạy từ thư mục gốc của lab):
    python grade.py

Cách tính điểm (tổng 100):
    - 5 nhóm test (75đ): điểm mỗi nhóm = số test pass / tổng test * điểm nhóm
    - exercises.md (25đ): điểm = số câu đã trả lời / tổng số câu * 25
      (một câu tính là "đã trả lời" khi dòng '> *Câu trả lời của bạn*' của
       câu đó đã được thay bằng nội dung khác)

Ưu tiên chấm solution/solution.py và solution/exercises.md nếu tồn tại,
nếu không sẽ chấm template.py và exercises.md ở thư mục gốc.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

DAY_DIR = Path(__file__).parent

# (tên tiêu chí, args pytest, điểm tối đa)
TEST_GROUPS = [
    ("CP1 — Part 1: API cơ bản", ["tests/test_part1.py"], 15),
    ("CP2 — Part 2: System prompt & token", ["tests/test_part2.py"], 15),
    ("CP3 — Part 3: Streaming & retry", ["tests/test_part3.py"], 15),
    ("CP4 — Part 4: Mini-project cơ bản", ["tests/test_part4.py", "-k", "Basic"], 15),
    ("Demo — Kịch bản hội thoại tự động", ["tests/test_part4.py", "-k", "Scenario"], 15),
]

EXERCISES_POINTS = 25
# Mỗi câu hỏi có đúng một dòng trả lời dạng '> *Câu trả lời của bạn*'.
# Phải so khớp cả tiền tố '> ': cụm placeholder còn xuất hiện trong phần hướng
# dẫn ở đầu exercises.md, nên nếu đếm cả dòng đó thì bài đã trả lời đủ 9 câu
# vẫn bị tính là thiếu một câu.
ANSWER_PLACEHOLDER = "> *Câu trả lời của bạn*"
TOTAL_QUESTIONS = 9  # số câu hỏi trong exercises.md gốc


class _Collector:
    """Plugin pytest đếm số test pass/fail trong một lần chạy."""

    def __init__(self):
        self.passed = 0
        self.total = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.total += 1
            if report.passed:
                self.passed += 1
        elif report.failed:
            # Lỗi ở setup (ví dụ: file không import được) — tính là 1 test rớt
            self.total += 1


def run_test_group(pytest_args: list[str]) -> tuple[int, int]:
    """Chạy một nhóm test, trả về (số pass, tổng số)."""
    resolved = [
        str(DAY_DIR / arg) if arg.startswith("tests/") else arg
        for arg in pytest_args
    ]
    collector = _Collector()
    pytest.main(
        resolved + ["-q", "--tb=no", "--no-header", "-p", "no:cacheprovider"],
        plugins=[collector],
    )
    return collector.passed, collector.total


def _rel(path: Path | None) -> str:
    """Đường dẫn tương đối so với thư mục lab, để in cho gọn."""
    return str(path.relative_to(DAY_DIR)) if path else "(không tìm thấy)"


def resolve_targets() -> tuple[Path | None, Path | None]:
    """Trả về (file code, file exercises) sẽ được chấm.

    Thứ tự ưu tiên giống hệt tests/_loader.py: bản trong solution/ thắng bản ở
    thư mục gốc. In ra để bạn không lỡ chấm nhầm một bản copy đã cũ.
    """
    code = next(
        (p for p in (DAY_DIR / "solution" / "solution.py", DAY_DIR / "template.py")
         if p.exists()),
        None,
    )
    exercises = next(
        (p for p in (DAY_DIR / "solution" / "exercises.md", DAY_DIR / "exercises.md")
         if p.exists()),
        None,
    )
    return code, exercises


def grade_exercises() -> tuple[int, Path | None]:
    """Trả về (số câu đã trả lời, đường dẫn file được chấm)."""
    _, candidate = resolve_targets()
    if candidate is None:
        return 0, None
    remaining = sum(
        1
        for line in candidate.read_text(encoding="utf-8").splitlines()
        if line.strip() == ANSWER_PLACEHOLDER
    )
    return max(0, TOTAL_QUESTIONS - remaining), candidate


def main() -> int:
    print("=" * 70)
    print("CHẤM ĐIỂM TỰ ĐỘNG — K4 Ngày 1: Khám Phá LLM API")
    print("=" * 70)

    code_file, ex_file = resolve_targets()
    print(f"Đang chấm code:      {_rel(code_file)}")
    print(f"Đang chấm exercises: {_rel(ex_file)}")

    rows = []

    for name, args, max_points in TEST_GROUPS:
        print(f"\n>>> {name}")
        passed, total = run_test_group(args)
        score = round(max_points * passed / total, 1) if total else 0.0
        rows.append((name, f"{passed}/{total} test", score, max_points))

    answered, exercises_file = grade_exercises()
    ex_score = round(EXERCISES_POINTS * answered / TOTAL_QUESTIONS, 1)
    detail = (
        f"{answered}/{TOTAL_QUESTIONS} câu"
        if exercises_file
        else "không tìm thấy exercises.md"
    )
    rows.append(("Exercises — câu hỏi phản ánh", detail, ex_score, EXERCISES_POINTS))

    print("\n" + "=" * 70)
    print("BẢNG ĐIỂM")
    print("=" * 70)
    total_score = 0.0
    for name, detail, score, max_points in rows:
        total_score += score
        print(f"  {name:<38} {detail:<22} {score:>5.1f}/{max_points}")
    print("-" * 70)
    print(f"  {'TỔNG':<38} {'':<22} {round(total_score, 1):>5.1f}/100")
    print("=" * 70)
    print(
        "Ghi chú: điểm exercises là điểm hoàn thành — chất lượng nội dung\n"
        "có thể được giảng viên điều chỉnh khi chấm lại thủ công."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
