CREATE TABLE IF NOT EXISTS analyses
(
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    query TEXT NOT NULL
);

ALTER TABLE analyses
    ADD CONSTRAINT analyses_unique_name UNIQUE (name);