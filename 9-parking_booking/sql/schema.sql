CREATE TABLE IF NOT EXISTS spots (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL,
    covered INTEGER NOT NULL,
    daily_rate REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    spot_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (spot_id) REFERENCES spots(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
