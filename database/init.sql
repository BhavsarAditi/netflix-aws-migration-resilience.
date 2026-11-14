-- StreamFlix demo schema. The Flask migration service creates and seeds
-- catalog rows on startup; these tables are also documented here for review.
CREATE TABLE IF NOT EXISTS playback_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    movie_id INTEGER,
    profile_name VARCHAR(80) DEFAULT 'Aditi',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS service_health (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    checked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
