import psycopg2

# This file creates the database schema + inserts data
# Good for resetting lab state quickly

conn = psycopg2.connect(
    dbname="sql_lab",
    user="postgres",
    password="postgres",
    host="localhost"
)

cur = conn.cursor()

# Drop table if re-running
cur.execute("DROP TABLE IF EXISTS users")

# Create simple table
cur.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        tenant_id INT NOT NULL
    )
""")

# Insert sample users
cur.execute("""
    INSERT INTO users (username, password, tenant_id) VALUES
    ('bob.martins', 'sup34r4ser20$', 2),
    ('cassandra.profs', '$1KmagicH4t20', 2),
    ('timmy.kanny', 'ad$min@tres', 1)
""")

conn.commit()
cur.close()
conn.close()
