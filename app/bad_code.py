"""Плохо написанная функция для расчёта прогресса тренировки."""


def calc(a, b, c, d, e, f, g, h):
    """Рассчитывает какой-то прогресс..."""
    # магические числа и непонятные переменные
    x = a * 2.5
    y = b + c * 0.3
    z = d / 3 if d != 0 else 1
    w = e * 1.2 - f * 0.8
    v = g + h * 0.5

    # дублирование кода
    if x > 100:
        x = x * 1.1
    if y > 100:
        y = y * 1.1
    if z > 100:
        z = z * 1.1
    if w > 100:
        w = w * 1.1
    if v > 100:
        v = v * 1.1

    # ещё магические числа
    r1 = (x + y) / 2 * 0.7
    r2 = (z + w) / 2 * 0.7
    r3 = v * 0.3
    # ... много строк дублирования
    total = r1 + r2 + r3
    if total > 250:
        total = total * 0.85
    if total < 50:
        total = total * 1.2
    bonus = 0
    if x > 80:
        bonus += 10
    if y > 80:
        bonus += 10
    if z > 80:
        bonus += 10
    if w > 80:
        bonus += 10
    if v > 80:
        bonus += 10
    total = total + bonus
    # нет docstring, нет type hints, нет обработки ошибок
    return round(total, 2)