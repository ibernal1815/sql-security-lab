# SQL Security Lab

This repository is a personal project created to explore SQL security practices using PostgreSQL and Flask. It is not a tutorial or production-ready application, but rather a learning artifact documenting experiments with SQL injection, secure query patterns, and database hardening.

---

## Purpose

The goal of this lab is to gain hands-on experience with:

- Understanding SQL injection vulnerabilities and exploitation
- Implementing secure query patterns using parameterized SQL
- Using PostgreSQL role-based access control
- Enabling Row-Level Security (RLS) for tenant isolation
- Monitoring PostgreSQL using `pg_stat_statements`
- Enforcing SSL and SCRAM-SHA-256 authentication
- Applying least-privilege principles

---

## Project Structure

sql_security_lab/
├── app/
│ ├── config.py # Database configuration / environment loading
│ ├── db.py # Secure and insecure DB connection helpers
│ ├── seed.py # Initializes schema and seeds data
├── database/
│ ├── roles.sql # Defines database roles and permissions
│ ├── schema.sql # Defines the application schema
│ ├── seed_data.sql # Inserts sample user data
├── scripts/
│ ├── start_postgres.sh # Script to start PostgreSQL service
│ ├── init_db.sh # Wrapper for running SQL setup scripts
├── vulnerable_app.py # Insecure Flask app (vulnerable to SQLi)
├── secure_app.py # Secure Flask app (parameterized queries)
├── requirements.txt # Python dependencies
├── .env # Environment file for DB credentials
└── README.md # Project documentation

markdown
Copy code

---

## Phase Overview

This project is separated into four phases:

### Phase 1: Insecure App
- Create a basic Flask app that connects to PostgreSQL
- Implement a login form vulnerable to SQL injection
- Insert sample users into the database
- Use `vulnerable_app.py` to demonstrate an injection attack (e.g. `' OR TRUE --`)

### Phase 2: Database Hardening
- Create distinct roles: `app_user`, `app_reader`, `admin`
- Use least-privilege access controls
- Remove superuser privileges from `app_user`
- Revoke default privileges
- Configure SCRAM-SHA-256 authentication and enforce SSL

### Phase 3: Secure App
- Implement `secure_app.py` using parameterized queries
- Use proper role and SSL context in DB connection
- Enable basic user isolation with a `tenant_id` field
- Optionally apply Row-Level Security (RLS)

### Phase 4: Monitoring and Performance
- Enable `pg_stat_statements` in `postgresql.conf`
- Query execution stats to monitor access patterns
- Review tracked queries from `secure_app.py` and `vulnerable_app.py`

---

## Screenshots
Screenshots for each phase can be found in `/screenshots`:

- `phase1_injection_demo.png`
- `phase2_roles_permissions.png`
- `phase2_ssl_config.png`
- `phase3_secure_app_login.png`
- `phase4_pg_stat_activity.png`

---

## Requirements

### System
- Linux Mint or Ubuntu VM
- PostgreSQL (tested with version 14+)
- Python3 and virtualenv

### Python Libraries
Install using:

pip install -r requirements.txt

yaml
Copy code

Minimal set includes:
- Flask
- psycopg2-binary
- python-dotenv

---

## Setup

1. Clone the repository:

git clone https://github.com/yourname/sql_security_lab.git
cd sql_security_lab

cpp
Copy code

2. Start your virtual environment:

python3 -m venv venv
source venv/bin/activate

markdown
Copy code

3. Initialize database:

sudo -u postgres psql -f database/roles.sql
sudo -u postgres psql -f database/schema.sql
sudo -u postgres psql -f database/seed_data.sql

markdown
Copy code

4. Run the secure or vulnerable app:

python vulnerable_app.py

or
python secure_app.py

yaml
Copy code

---

## Key Learnings

- Unsafe query construction opens the door for SQL injection
- Parameterized queries mitigate injection entirely
- Least privilege roles help minimize damage from compromised web apps
- PostgreSQL Row-Level Security enables powerful tenant isolation
- Monitoring with `pg_stat_statements` supports both security and optimization

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Notes

- This is an educational project; do not deploy in production
- All testing was performed on an isolated VM
- Feel free to fork or modify for your own learning
