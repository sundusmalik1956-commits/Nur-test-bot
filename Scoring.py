# -*- coding: utf-8 -*-
"""
منطق حساب الدرجات وتحديد المستوى اللغوي بدون أي ذكاء اصطناعي.
"""

TOTAL_QUESTIONS = 9

LEVELS = {
    "A1": {"ar": "A1 (مبتدئ)", "en": "A1 (Beginner)"},
    "A2": {"ar": "A2 (متوسط أدنى)", "en": "A2 (Elementary)"},
    "B1": {"ar": "B1 (متوسط)", "en": "B1 (Intermediate)"},
    "B2": {"ar": "B2 (متقدم)", "en": "B2 (Upper Intermediate)"},
}


def calculate_score(correct_count: int, total: int = TOTAL_QUESTIONS) -> int:
    """يحسب الدرجة من 100 بناءً على عدد الإجابات الصحيحة."""
    if total <= 0:
        return 0
    score = round((correct_count / total) * 100)
    return min(score, 100)


def determine_level(correct_count: int) -> str:
    """
    يحدد المستوى بناءً على عدد الإجابات الصحيحة (من أصل 9)
    وفق المعيار المحدد:
      A1: 0-4 صحيحة (0-44 درجة)
      A2: 5-6 صحيحة (45-65 درجة)
      B1: 7-8 صحيحة (66-85 درجة)
      B2: 9 صحيحة   (86-100 درجة)
    """
    if correct_count <= 4:
        return "A1"
    elif correct_count <= 6:
        return "A2"
    elif correct_count <= 8:
        return "B1"
    else:
        return "B2"


def get_level_label(level_code: str, lang: str) -> str:
    """يعيد اسم المستوى مترجماً (نستخدم نفس رمز المستوى القياسي CEFR لكل اللغات مع وصف مختصر)."""
    entry = LEVELS.get(level_code, {})
    return entry.get(lang) or entry.get("en") or level_code
