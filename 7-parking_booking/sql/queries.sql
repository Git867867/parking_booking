-- =====================================================
-- Запрос 1. Список всех парковочных мест (SELECT)
-- Используется на странице /spots/
-- =====================================================
SELECT id, number, covered, daily_rate
FROM spots
ORDER BY number;

-- =====================================================
-- Запрос 2. Крытые места (WHERE)
-- Используется на странице /spots/?covered=1
-- =====================================================
SELECT id, number, covered, daily_rate
FROM spots
WHERE covered = 1
ORDER BY daily_rate;

-- =====================================================
-- Запрос 3. Открытые места (WHERE)
-- Используется на странице /spots/?covered=0
-- =====================================================
SELECT id, number, covered, daily_rate
FROM spots
WHERE covered = 0
ORDER BY daily_rate;

-- =====================================================
-- Запрос 4. Активные бронирования (JOIN + WHERE)
-- Используется на странице /bookings/
-- =====================================================
SELECT b.id,
       b.start,
       b.end,
       s.number AS spot_number,
       u.name AS user_name
FROM bookings b
JOIN spots s ON b.spot_id = s.id
JOIN users u ON b.user_id = u.id
WHERE b.is_cancelled = 0
ORDER BY b.start;

-- =====================================================
-- Запрос 5. Полная информация о бронировании (JOIN + WHERE)
-- Используется на странице /bookings/<id>/
-- В Django вместо 1 передаётся параметр ?
-- =====================================================
SELECT b.id,
       b.start,
       b.end,
       b.is_cancelled,
       s.number AS spot_number,
       s.daily_rate,
       u.name AS user_name
FROM bookings b
JOIN spots s ON b.spot_id = s.id
JOIN users u ON b.user_id = u.id
WHERE b.id = 1;

-- =====================================================
-- Запрос 6. Свободные места на выбранную дату (подзапрос)
-- Используется на странице /spots/available/?date=...
-- В Django вместо даты передаётся параметр ?
-- =====================================================
SELECT id, number, covered, daily_rate
FROM spots
WHERE id NOT IN (
    SELECT spot_id
    FROM bookings
    WHERE start <= '2026-09-22'
      AND end >= '2026-09-22'
      AND is_cancelled = 0
)
ORDER BY number;

-- =====================================================
-- Запрос 7. Количество активных бронирований (COUNT)
-- Используется на странице /bookings/statistics/
-- =====================================================
SELECT COUNT(*) AS bookings_count
FROM bookings
WHERE is_cancelled = 0;

-- =====================================================
-- Запрос 8. Средняя стоимость места (AVG)
-- Используется на странице /bookings/statistics/
-- =====================================================
SELECT AVG(daily_rate) AS avg_rate
FROM spots;

-- =====================================================
-- Запрос 9. Максимальная стоимость места (MAX)
-- Используется на странице /bookings/statistics/
-- =====================================================
SELECT MAX(daily_rate) AS max_rate
FROM spots;

-- =====================================================
-- Запрос 10. Количество бронирований по местам (GROUP BY)
-- Используется на странице /bookings/statistics/
-- =====================================================
SELECT s.number AS spot_number,
       COUNT(b.id) AS bookings_count
FROM spots s
LEFT JOIN bookings b ON s.id = b.spot_id AND b.is_cancelled = 0
GROUP BY s.id, s.number
ORDER BY bookings_count DESC;

-- =====================================================
-- Запрос 11. Места с количеством бронирований больше 1 (HAVING)
-- Используется на странице /bookings/statistics/
-- =====================================================
SELECT s.number AS spot_number,
       COUNT(b.id) AS bookings_count
FROM spots s
JOIN bookings b ON s.id = b.spot_id
WHERE b.is_cancelled = 0
GROUP BY s.id, s.number
HAVING COUNT(b.id) > 1
ORDER BY bookings_count DESC;
