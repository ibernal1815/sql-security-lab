# sql-security-lab

Two Flask apps, one PostgreSQL database, and one question. How bad does it actually get when you skip input validation?

I built this to stop treating SQL injection as a concept and start treating it as something I could demonstrate, measure, and fix. The lab runs both a vulnerable and a hardened version of the same application side by side so the difference is not theoretical. You can watch the attack work, then watch it fail.

## Background / Why I Built This

SQL injection consistently tops vulnerability lists and has for decades. Every security course covers it but most of the time you see it as a one-liner example in a slide. I wanted to actually build the vulnerable app, run the attack myself, and then harden it layer by layer. Not just patch the query, but lock down the database the way you would in a real environment.

So I built both versions. vulnerable_app.py has the broken login. secure_app.py has parameterized queries, role-based access control, Row-Level Security, and SSL enforcement. Same schema, same data, completely different posture.

## What It Does

**Phase 1 — Vulnerable App**
A Flask login form backed by PostgreSQL that builds queries with raw string concatenation. A classic `' OR TRUE --` bypasses authentication entirely. The point is to see it work, not just read about it.

**Phase 2 — Database Hardening**
Three PostgreSQL roles with least-privilege access: app_user, app_reader, and admin. Superuser privileges stripped from the app user. SCRAM-SHA-256 authentication enforced. SSL required. Default privileges revoked.

**Phase 3 — Secure App**
Same login flow, rewritten with parameterized queries and the correct role in the connection context. Row-Level Security enabled so users can only access their own rows regardless of what the query looks like. Injection attempts return nothing.

**Phase 4 — Monitoring**
pg_stat_statements enabled to track query execution patterns across both apps. Useful for seeing exactly what queries each version is running and where the attack surface was.

## Project Layout

```
sql_security_lab/
├── app/
│   ├── config.py
│   ├── db.py
│   └── seed.py
├── database/
│   ├── roles.sql
│   ├── schema.sql
│   └── seed_data.sql
├── scripts/
│   ├── start_postgres.sh
│   └── init_db.sh
├── vulnerable_app.py
├── secure_app.py
├── requirements.txt
└── .env
```

## Setup

```bash
git clone https://github.com/ibernal1815/sql-security-lab.git
cd sql-security-lab

python3 -m venv venv
source venv/bin/activate

sudo -u postgres psql -f database/roles.sql
sudo -u postgres psql -f database/schema.sql
sudo -u postgres psql -f database/seed_data.sql
```

Run the vulnerable app:

```bash
python vulnerable_app.py
```

Run the secure app:

```bash
python secure_app.py
```

## Stack

Python 3 · Flask · PostgreSQL · psycopg2 · pg_stat_statements
