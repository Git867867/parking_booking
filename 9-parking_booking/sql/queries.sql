SELECT id, number, covered, daily_rate FROM spots ORDER BY number;

SELECT id, number, covered, daily_rate FROM spots WHERE covered = 1 ORDER BY daily_rate;

SELECT b.id, b.start, b.end, s.number AS spot_number, u.name AS user_name
FROM bookings b
JOIN spots s ON b.spot_id = s.id
JOIN users u ON b.user_id = u.id
WHERE b.is_cancelled = 0
ORDER BY b.start;

SELECT id, number, covered, daily_rate
FROM spots
WHERE id NOT IN (
    SELECT spot_id FROM bookings
    WHERE start <= '2026-09-22' AND end >= '2026-09-22' AND is_cancelled = 0
)
ORDER BY number;

SELECT COUNT(*) AS bookings_count FROM bookings WHERE is_cancelled = 0;

SELECT AVG(daily_rate) AS avg_rate FROM spots;

SELECT MAX(daily_rate) AS max_rate FROM spots;

SELECT s.number AS spot_number, COUNT(b.id) AS bookings_count
FROM spots s
LEFT JOIN bookings b ON s.id = b.spot_id AND b.is_cancelled = 0
GROUP BY s.id, s.number
ORDER BY bookings_count DESC;
