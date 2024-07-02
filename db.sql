--Table Creation
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PgSQL Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.name IS DISTINCT FROM OLD.name OR
       NEW.category IS DISTINCT FROM OLD.category OR
       NEW.amount IS DISTINCT FROM OLD.amount OR
       NEW.date IS DISTINCT FROM OLD.date THEN
        
          NEW.updated_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- PgSQL Trigger
CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON expense
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

