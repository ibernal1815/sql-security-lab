-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tenant_id INTEGER NOT NULL
);

-- Create tenants table
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Enable Row-Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy so users can only see their data
CREATE POLICY tenant_isolation_policy ON users
    FOR SELECT
    USING (tenant_id = current_setting('app.current_tenant')::integer);
