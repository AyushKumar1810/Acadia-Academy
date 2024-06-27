-- create_tables.sql
-- Create Sales Table
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    sale_date TEXT,
    customer_id INTEGER,
    sale_amount REAL
);

-- Create Returns Table
CREATE TABLE IF NOT EXISTS Returns (
    return_id INTEGER PRIMARY KEY,
    sale_id INTEGER,
    return_date TEXT,
    return_amount REAL,
    sale_amount REAL
);
