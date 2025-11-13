-- V2__alter_table.sql
-- Add email column and create indexes

-- Add email column
ALTER TABLE subscribers 
ADD COLUMN email VARCHAR(255) UNIQUE AFTER phone;

-- Update existing records with sample email addresses
UPDATE subscribers 
SET email = CONCAT(LOWER(first_name), '.', LOWER(last_name), '@example.com');

-- Create indexes for better query performance
CREATE INDEX idx_last_name ON subscribers(last_name);
CREATE INDEX idx_email ON subscribers(email);