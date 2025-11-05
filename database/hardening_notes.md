# PostgreSQL Hardening Notes

This file explains how I set up and secured PostgreSQL for my SQL Security Lab project.  
I made this as part of learning how to protect databases against attacks like SQL injection and to understand how authentication, encryption, and user permissions work.

---

## Project Overview

This was a local PostgreSQL setup (on Linux Mint/Ubuntu).  
The goal was to keep it locked down, safe to experiment with, and close to what a secure production setup should look like.

**Main security goals:**
- Stop outside connections and keep everything local.
- Use strong password protection and encryption.
- Only give users the access they really need.
- Prevent SQL injection and risky queries.
- Keep logs and backups in case something breaks.

---

## Network Setup

The database only listens on the local computer. That means no one outside can connect:

```
listen_addresses = 'localhost'
port = 5432
```

If remote access is ever needed for testing, it should be allowed only for specific IPs through a firewall:

```
sudo ufw default deny incoming
sudo ufw allow from 192.168.56.1 to any port 5432 proto tcp
```

---

## Authentication Settings

PostgreSQL checks who’s connecting using the `pg_hba.conf` file.  
I used peer authentication for the local admin user and SCRAM for everything else:

```
local   all   all                           peer
host    all   all   127.0.0.1/32            scram-sha-256
host    all   all   ::1/128                 scram-sha-256
```

SCRAM-SHA-256 is stronger than the old MD5 system, and this setting makes PostgreSQL use it by default:

```
password_encryption = scram-sha-256
```

---

## Enabling SSL (Encrypted Connections)

I turned on SSL so that if I ever connect over a network, the traffic is encrypted.

Steps I took:
```
sudo chown postgres:postgres /etc/postgresql/ssl/server.key
sudo chmod 600 /etc/postgresql/ssl/server.key
sudo chown postgres:postgres /etc/postgresql/ssl/server.crt
sudo chmod 644 /etc/postgresql/ssl/server.crt
```

Then I added this to `postgresql.conf`:
```
ssl = on
ssl_cert_file = '/etc/postgresql/ssl/server.crt'
ssl_key_file  = '/etc/postgresql/ssl/server.key'
```

And the app connects using:
```
sslmode=require
```

---

## Roles and Permissions (Least Privilege)

I didn’t use the main `postgres` superuser for my apps.  
Instead, I made smaller roles with only the permissions they actually need.

```
CREATE ROLE app_read NOINHERIT;
CREATE ROLE app_write NOINHERIT;

GRANT CONNECT ON DATABASE myappdb TO app_read, app_write;
GRANT USAGE ON SCHEMA public TO app_read, app_write;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_read;

GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_write;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE, DELETE ON TABLES TO app_write;

CREATE ROLE myappuser LOGIN PASSWORD 'REDACTED';
GRANT app_read, app_write TO myappuser;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
```

This setup means:
- The app can’t mess with database structure.
- It can only read or write where it’s supposed to.
- Even if the app gets hacked, the attacker is limited.

---

## Row-Level Security (RLS)

To simulate a multi-tenant app (like one database for many users), I used RLS.  
It lets PostgreSQL automatically filter which rows a user can see based on a “tenant” setting.

```
CREATE OR REPLACE FUNCTION current_tenant() RETURNS int
LANGUAGE sql STABLE AS $$ SELECT current_setting('app.current_tenant')::int $$;

ALTER TABLE users  ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY users_tenant_isolation
  ON users  USING (tenant_id = current_tenant());

CREATE POLICY orders_tenant_isolation
  ON orders USING (tenant_id = current_tenant());
```

The app tells PostgreSQL which tenant is active:
```
SET app.current_tenant = '1';
```

This is a strong way to separate user data at the database level.

---

## Safe Query Practices

In the secure version of my Flask app, every query uses parameters instead of string concatenation.

```
cur.execute(
    "SELECT id, username, email FROM users WHERE username = %s;",
    (username,)
)
```

Why it matters:
- Prevents SQL injection completely.
- Makes the code easier to maintain.
- Forces PostgreSQL to handle escaping safely.

---

## Logging and Auditing

I turned on PostgreSQL’s logging to track what’s going on:

```
logging_collector = on
log_statement = 'ddl'
log_min_duration_statement = 500
log_connections = on
log_disconnections = on
log_line_prefix = '%m [%p] %u@%d %h '
```

I also used the `pg_stat_statements` extension to monitor which queries run the most:

```
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

Logs go to `/var/log/postgresql/`.

---

## Indexes and Performance

I added indexes to speed up common lookups:

```
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_amount_big ON orders(amount) WHERE amount > 75;
```

Then I checked improvements using:
```
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2;
```

Indexes make queries faster and reduce database load.

---

## Backups and Restore Tests

Practiced creating and restoring backups:

```
pg_dump -h 127.0.0.1 -U myappuser -Fc -f /tmp/myappdb.dump myappdb
pg_restore -h 127.0.0.1 -U myappuser -d myappdb_restore /tmp/myappdb.dump
```

After restoring, I compared row counts to make sure everything copied correctly.

---

## Operating System Security

- `/var/lib/postgresql/` is owned by `postgres:postgres`
- `/etc/postgresql/` configs can only be changed by `root` or `postgres`
- SSH login uses keys instead of passwords
- PostgreSQL and OS packages are kept up to date

---

## Quick Security Checklist

| Check | Description |
|-------|--------------|
| ✅ Only localhost connections | No external exposure |
| ✅ SCRAM-SHA-256 | Strong password hashing |
| ✅ SSL enabled | Data encrypted in transit |
| ✅ Limited roles | App runs with least privilege |
| ✅ Parameterized queries | Stops SQL injection |
| ✅ RLS | Tenant-level data separation |
| ✅ Logging active | Tracks connections and slow queries |
| ✅ Backups tested | Verified restore works |

---

## Summary

This project helped me understand how real database hardening works.  
By combining:
- local-only access,
- strong authentication and encryption,
- least-privilege roles,
- parameterized queries,
- logging, and
- regular backups,

I built a PostgreSQL setup that’s secure, efficient, and realistic enough for learning professional cybersecurity and DevSecOps practices.
