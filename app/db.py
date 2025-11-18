import psycopg2
import psycopg2.extras
from flask import session

# This file exists so the app can import DB logic cleanly

def get_connection():
    # Uses role with limited rights
    tenant = session.get("tenant_id", 0)

    # options passes tenant to PostgreSQL session variable
    return psycopg2.connect(
        dbname="sql_lab",
        user="app_user",
        password="app_user_pass",
        host="localhost",
        options=f"-c app.current_tenant={tenant}"
    )
