"""
Задание 10: Генерация регулярного выражения

Задача валидации: ID тренировки (Workout ID) для платформы спортивных тренировок.
Формат: 3 заглавные буквы (латиница) + дефис + 4 цифры.
Пример валидного ID: WRK-0001, FIT-1234, CRO-9999
Пример невалидного ID: wrk-0001 (строчные буквы), FIT-123 (3 цифры),
WORK-0001 (4 буквы), FIT_1234 (неверный разделитель)
"""

import re
from typing import List

# Регулярное выражение для валидации ID тренировки
# ^ - начало строки
# [A-Z]{3} - ровно 3 заглавные латинские буквы
# - - дефис
# \d{4} - ровно 4 цифры
# $ - конец строки
WORKOUT_ID_PATTERN = r"^[A-Z]{3}-\d{4}$"

workout_id_regex = re.compile(WORKOUT_ID_PATTERN)


def is_valid_workout_id(workout_id: str) -> bool:
    """
    Проверяет, является ли строка валидным ID тренировки.

    Args:
        workout_id: Строка для проверки.

    Returns:
        True, если строка соответствует формату XXX-1234.
    """
    return bool(workout_id_regex.match(workout_id))


# =====================================================================
# ТЕСТИРОВАНИЕ
# =====================================================================

VALID_EXAMPLES: List[str] = [
    "WRK-0001",
    "FIT-1234",
    "CRO-9999",
    "ABC-0000",
    "XYZ-5678",
]

INVALID_EXAMPLES: List[str] = [
    "wrk-0001",    # строчные буквы
    "FIT-123",     # 3 цифры вместо 4
    "WORK-0001",   # 4 буквы вместо 3
    "FIT_1234",    # подчёркивание вместо дефиса
    "FIT-12 34",   # пробел внутри
    " FI-1234",    # пробел в начале
    "FIT-12345",   # 5 цифр вместо 4
    "fit-1234",    # все строчные
    "123-4567",    # цифры вместо букв
    "",            # пустая строка
]


def run_tests() -> None:
    """Запускает тестирование регулярного выражения."""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РЕГУЛЯРНОГО ВЫРАЖЕНИЯ")
    print(f"Паттерн: {WORKOUT_ID_PATTERN}")
    print("=" * 60)

    print("\nВАЛИДНЫЕ ПРИМЕРЫ:")
    all_valid_passed = True
    for example in VALID_EXAMPLES:
        result = is_valid_workout_id(example)
        status = "✓" if result else "✗"
        if not result:
            all_valid_passed = False
        print(f"  {status} '{example}' -> {result}")

    print("\nНЕВАЛИДНЫЕ ПРИМЕРЫ:")
    all_invalid_passed = True
    for example in INVALID_EXAMPLES:
        result = is_valid_workout_id(example)
        status = "✓" if not result else "✗"
        if result:
            all_invalid_passed = False
        print(f"  {status} '{example}' -> {result}")

    print("\n" + "=" * 60)
    if all_valid_passed and all_invalid_passed:
        print("РЕЗУЛЬТАТ: Все тесты пройдены!")
    else:
        print("РЕЗУЛЬТАТ: Некоторые тесты не пройдены!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()