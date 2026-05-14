"""
Рефакторинг плохо написанной функции calc().

Исходная функция рассчитывала 'прогресс тренировки' на основе 8 параметров,
но была написана с рядом проблем:
1. Длина функции > 30 строк (42 строки)
2. Магические числа (2.5, 0.3, 1.2, 0.8, 0.7, 0.85, 1.1, 10, 50, 80, 100, 250)
3. Отсутствие обработки ошибок (деление на ноль обработано, но нет проверки типов)
4. Неинформативные имена переменных (calc, a, b, c, x, y, z, w, v, r1, r2, r3)
5. Дублирование кода (5 раз повторяется один и тот же блок if x > 100: x = x * 1.1)
6. Отсутствие type hints
7. Непонятная бизнес-логика без документации
"""


def calculate_training_progress(
    strength_score: float,
    endurance_score: float,
    flexibility_score: float,
    speed_score: float,
    accuracy_score: float,
    recovery_score: float,
    consistency_score: float,
    intensity_score: float,
) -> float:
    """
    Рассчитывает общий прогресс тренировки на основе 8 метрик.

    Алгоритм:
    1. Взвешивание метрик с разными коэффициентами важности.
    2. Применение бонусного множителя для высоких значений (>100).
    3. Расчёт промежуточных групп показателей.
    4. Итоговая нормализация и применение корректирующих коэффициентов.
    5. Добавление бонусных очков за метрики выше порога (80).

    Args:
        strength_score: Оценка силы (0-200)
        endurance_score: Оценка выносливости (0-200)
        flexibility_score: Оценка гибкости (0-200)
        speed_score: Оценка скорости (0-200)
        accuracy_score: Оценка точности (0-200)
        recovery_score: Оценка восстановления (0-200)
        consistency_score: Оценка регулярности (0-200)
        intensity_score: Оценка интенсивности (0-200)

    Returns:
        Итоговый прогресс тренировки (0-1000)

    Raises:
        ValueError: Если любой из показателей отрицательный
    """
    # Валидация входных данных
    scores = [
        strength_score, endurance_score, flexibility_score,
        speed_score, accuracy_score, recovery_score,
        consistency_score, intensity_score,
    ]
    for score in scores:
        if score < 0:
            raise ValueError(f"Оценка не может быть отрицательной: {score}")

    # Коэффициенты важности для каждой метрики
    STRENGTH_WEIGHT = 2.5
    ENDURANCE_WEIGHT = 0.3
    FLEXIBILITY_DIVISOR = 3.0
    SPEED_WEIGHT = 1.2
    ACCURACY_WEIGHT = 0.8
    RECOVERY_WEIGHT = 0.5
    HIGH_SCORE_THRESHOLD = 100.0
    HIGH_SCORE_MULTIPLIER = 1.1
    BONUS_THRESHOLD = 80.0
    BONUS_POINTS = 10
    TOTAL_UPPER_BOUND = 250.0
    TOTAL_LOWER_BOUND = 50.0
    UPPER_CORRECTION = 0.85
    LOWER_CORRECTION = 1.2

    # Расчёт взвешенных метрик
    weighted_strength = strength_score * STRENGTH_WEIGHT
    weighted_endurance = endurance_score + flexibility_score * ENDURANCE_WEIGHT
    weighted_flexibility = (
        speed_score / FLEXIBILITY_DIVISOR if speed_score != 0 else 1.0
    )
    weighted_speed = speed_score * SPEED_WEIGHT - accuracy_score * ACCURACY_WEIGHT
    weighted_accuracy = recovery_score + intensity_score * RECOVERY_WEIGHT

    # Применение бонусного множителя для высоких значений
    weighted_scores = [
        weighted_strength,
        weighted_endurance,
        weighted_flexibility,
        weighted_speed,
        weighted_accuracy,
    ]
    adjusted_scores = [
        score * HIGH_SCORE_MULTIPLIER if score > HIGH_SCORE_THRESHOLD else score
        for score in weighted_scores
    ]

    # Расчёт промежуточных групп
    POWER_GROUP_WEIGHT = 0.7
    power_group = (
        (adjusted_scores[0] + adjusted_scores[1]) / 2 * POWER_GROUP_WEIGHT
    )
    technique_group = (
        (adjusted_scores[2] + adjusted_scores[3]) / 2 * POWER_GROUP_WEIGHT
    )
    mental_group = adjusted_scores[4] * 0.3

    # Итоговый расчёт с коррекцией
    total = power_group + technique_group + mental_group
    if total > TOTAL_UPPER_BOUND:
        total *= UPPER_CORRECTION
    if total < TOTAL_LOWER_BOUND:
        total *= LOWER_CORRECTION

    # Бонусные очки за выдающиеся метрики
    bonus = sum(
        BONUS_POINTS for score in adjusted_scores if score > BONUS_THRESHOLD
    )
    total += bonus

    return round(total, 2)