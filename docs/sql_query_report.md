# Отчёт по SQL-запросам

## Задание 9: Генерация SQL-запросов

**Описание отчёта:** "Топ-10 упражнений по частоте выполнения за последние 30 дней"

### SQL-запрос (для PostgreSQL)

```sql
SELECT
    e.id AS exercise_id,
    e.name AS exercise_name,
    e.category,
    COUNT(we.workout_id) AS times_included,
    ROUND(AVG(p.score), 2) AS avg_progress_score
FROM exercises e
JOIN workout_exercises we ON e.id = we.exercise_id
JOIN workouts w ON we.workout_id = w.id
LEFT JOIN progress p ON e.id = p.exercise_id
    AND p.date >= CURRENT_DATE - INTERVAL '30 days'
WHERE w.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY e.id, e.name, e.category
ORDER BY times_included DESC
LIMIT 10;
```

### SQL-запрос (для SQLite)

```sql
SELECT
    e.id AS exercise_id,
    e.name AS exercise_name,
    e.category,
    COUNT(we.workout_id) AS times_included,
    ROUND(AVG(p.score), 2) AS avg_progress_score
FROM exercises e
JOIN workout_exercises we ON e.id = we.exercise_id
JOIN workouts w ON we.workout_id = w.id
LEFT JOIN progress p ON e.id = p.exercise_id
    AND p.date >= DATE('now', '-30 days')
WHERE w.created_at >= DATE('now', '-30 days')
GROUP BY e.id, e.name, e.category
ORDER BY times_included DESC
LIMIT 10;
```

### Объяснение логики запроса

1. **JOIN workout_exercises we ON e.id = we.exercise_id** — связывает упражнения с тренировками, в которые они включены. Именно эта таблица позволяет подсчитать, сколько раз каждое упражнение было использовано.

2. **JOIN workouts w ON we.workout_id = w.id** — получаем дату тренировки, чтобы отфильтровать по времени.

3. **LEFT JOIN progress p ON e.id = p.exercise_id AND p.date >= CURRENT_DATE - INTERVAL '30 days'** — LEFT JOIN, а не INNER JOIN, чтобы упражнения без записей прогресса тоже попали в результат (avg_progress_score будет NULL). Фильтр по дате перенесён в условие JOIN, чтобы не потерять упражнения, у которых есть тренировки, но нет прогресса.

4. **WHERE w.created_at >= CURRENT_DATE - INTERVAL '30 days'** — оставляем только тренировки за последние 30 дней.

5. **GROUP BY e.id, e.name, e.category** — группируем по уникальному упражнению.

6. **ORDER BY times_included DESC** — сортируем от самого популярного к наименее популярному.