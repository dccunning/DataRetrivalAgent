-- Create the database (run this outside the db, e.g., in psql or manually)
-- CREATE DATABASE dra_db;

-- Connect to the database (optional if already connected)
-- \c dra_db

-- Create schema
CREATE SCHEMA IF NOT EXISTS backend;

-- Create users table
CREATE TABLE IF NOT EXISTS backend.user (
    id SERIAL PRIMARY KEY,
    password BYTEA NOT NULL,
    email TEXT UNIQUE,
    role TEXT NOT NULL DEFAULT 'user',
    credentials_json BYTEA,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS backend.user_metadata (
    user_id INT PRIMARY KEY REFERENCES backend.user(id),
    manifest_json BYTEA,
    catalog_json BYTEA,
    table_summary_json BYTEA,
    table_descriptions_json BYTEA,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

