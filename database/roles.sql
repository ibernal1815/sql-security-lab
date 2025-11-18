-- Drop existing users for a clean slate
DROP ROLE IF EXISTS sql_user;
DROP ROLE IF EXISTS app_reader;
DROP ROLE IF EXISTS app_writer;

-- Create a main user role that owns the database
CREATE ROLE sql_user WITH
    LOGIN
    PASSWORD 'securepassword'
    CREATEDB
    NOSUPERUSER;

-- Application roles with limited privileges
CREATE ROLE app_reader NOLOGIN;
CREATE ROLE app_writer NOLOGIN;

-- Grant connection to the necessary roles
GRANT CONNECT ON DATABASE sql_lab TO sql_user;
GRANT CONNECT ON DATABASE sql_lab TO app_reader, app_writer;

-- Allow the reader to read permissions
GRANT USAGE ON SCHEMA public TO app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;

-- Allow the writer to insert, update, and delete
GRANT USAGE ON SCHEMA public TO app_writer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_writer;
