-- Create the database (run this outside the db, e.g., in psql or manually)
-- CREATE DATABASE dra_db;

-- Connect to the database (optional if already connected)
-- \c dra_db

-- Create schema
CREATE SCHEMA IF NOT EXISTS backend;

-- Create users table
CREATE TABLE IF NOT EXISTS backend.users (
    id SERIAL PRIMARY KEY,
    password BYTEA NOT NULL,
    email TEXT UNIQUE,
    role TEXT NOT NULL DEFAULT 'user',
    credentials_json BYTEA,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

