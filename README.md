# sql-security-lab

two Flask apps, one PostgreSQL database, and one question. how bad does it actually get when you skip input validation?

i built this to stop treating SQL injection as a concept and start treating it as something i could demonstrate, measure, and fix. the lab runs both a vulnerable and a hardened version of the same application side by side so the difference is not theoretical. you can watch the attack work, then watch it fail.

## background / why i built this

SQL injection consistently tops vulnerability lists and has for decades. every security course covers it but most of the time you see it as a one-liner example in a slide. i wanted to actually build the vulnerable app, run the attack myself, and then harden it layer by layer. not just patch the query, but lock down the database the way you would in a real environment.

so i built both versions. vulnerable_app.py has the broken login. secure_app.py has parameterized queries, role-based access control, Row-Level Security, and SSL enforcement. same schema, same data, completely different posture.

## what it does

**phase 1 — vulnerable app**
a Flask login form backed by PostgreSQL that builds queries with raw string concatenation. a classic `' OR TRUE --` bypasses authentication entirely. the point is to see it work, not just read about it.

**phase 2 — database hardening**
three PostgreSQL roles with least-privilege access: app_user, app_reader, and admin. superuser privileges stripped from the app user. SCRAM-SHA-256 authentication enforced. SSL required. default privileges revoked.

**phase 3 — secure app**
same login flow, rewritten with parameterized queries and the correct role in the connection context. Row-Level Security enabled so users can only access their own rows regardless of what the query looks like. injection attempts return nothing.

**phase 4 — monitoring**
pg_stat_statements enabled to track query execution patterns across both apps. useful for seeing exactly what queries each version is running and where the attack surface was.

## project layout

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

## setup

```bash
git clone https://github.com/ibernal1815/sql-security-lab.git
cd sql-security-lab

python3 -m venv venv
source venv/bin/activate

sudo -u postgres psql -f database/roles.sql
sudo -u postgres psql -f database/schema.sql
sudo -u postgres psql -f database/seed_data.sql
```

run the vulnerable app:

```bash
python vulnerable_app.py
```

run the secure app:

```bash
python secure_app.py
```

## stack

Python 3 · Flask · PostgreSQL · psycopg2 · pg_stat_statements
