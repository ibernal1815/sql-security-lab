# PostgreSQL Hardening Notes

This document outlines the security configuration and hardening steps implemented for the SQL Security Lab project. It serves as a technical record of the decisions made while setting up PostgreSQL in a secure, isolated environment. The goal was to understand and apply modern best practices for database security, authentication, encryption, and least-privilege design.

Scope: Local PostgreSQL instance used for development and testing of SQL security concepts. Objective: Build a secure baseline configuration resistant to unauthorized access, SQL injection, and privilege escalation. Environment: Single-node Linux setup (Mint/Ubuntu), not exposed to the public internet. Threats considered: Credential theft, SQL injection, network sniffing, and accidental privilege misuse.

PostgreSQL is bound only to the local interface:

```
listen_addresses = 'localhost'
port = 5432
```

No remote access is permitted by default. If remote access is ever needed, it should be restricted by subnet and controlled via firewall:

```
sudo ufw default deny incoming
sudo ufw allow from 192.168.56.1 to any port 5432 proto tcp
```

The host-based authentication file enforces modern password hashing and local peer authentication:

```
local   all   all                           peer
host    all   all   127.0.0.1/32            scram-sha-256
host    all   all   ::1/128                 scram-sha-256
```

Modern password encryption method enforced globally:

```
password_encryption = scram-sha-256
```

Peer authentication allows trusted local administrative access, while TCP connections require SCRAM-SHA-256, which replaces the older MD5 mechanism.

Self-signed certificates were created for SSL (lab use only):

```
sudo chown postgres:postgres /etc/postgresql/ssl/server.key
sudo chmod 600 /etc/postgresql/ssl/server.key
sudo chown postgres:postgres /etc/postgresql/ssl/server.crt
sudo chmod 644 /etc/postgresql/ssl/server.crt
```

Enabled SSL and pointed PostgreSQL to the certificate paths:

```
ssl = on
ssl_cert_file = '/etc/postgresql/ssl/server.crt'
ssl_key_file  = '/etc/postgresql/ssl/server.key'
```

All application connections enforce SSL mode:

```
sslmode=require
```

Encryption in transit ensures credentials and queries cannot be intercepted even within local or virtualized networks.

The `postgres` superuser is not used by any applications. Separate read/write roles and a login role for the app were created.

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

The application is limited to only the queries it requires. This prevents privilege misuse and reduces impact if the app is compromised.

Row-Level Security is used to demonstrate tenant data isolation via session variables.

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

Application sets tenant context per session:

```
SET app.current_tenant = '1';
```

Superusers and roles with `BYPASSRLS` can override these policies, so application roles must not have those privileges.

All queries in the secure app use parameterized statements:

```
cur.execute(
    "SELECT id, username, email FROM users WHERE username = %s;",
    (username,)
)
```

Inputs are type-validated (`Decimal`, `int`, etc.) before executing queries. No `SELECT *` is used in production-facing code. Parameterized queries ensure user input is treated as data, not executable SQL, completely neutralizing injection attacks.

Logging is enabled to capture meaningful events and slow queries.

```
logging_collector = on
log_statement = 'ddl'
log_min_duration_statement = 500
log_connections = on
log_disconnections = on
log_line_prefix = '%m [%p] %u@%d %h '
```

Query monitoring is enabled with `pg_stat_statements`:

```
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

Logs are rotated automatically under `/var/log/postgresql/`.

Indexes were created for common query paths and performance tested.

```
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_amount_big ON orders(amount) WHERE amount > 75;
```

Benchmarked using:

```
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2;
```

Optimized indexing improved execution time and mitigated the risk of long-running sequential scans.

Logical backups tested using `pg_dump` and `pg_restore`:

```
pg_dump -h 127.0.0.1 -U myappuser -Fc -f /tmp/myappdb.dump myappdb
pg_restore -h 127.0.0.1 -U myappuser -d myappdb_restore /tmp/myappdb.dump
```

Post-restore verification includes row count and constraint validation.

System-level permissions and ownership:

- `/var/lib/postgresql/` owned by `postgres:postgres`
- `/etc/postgresql/` configuration files writable only by root or postgres
- SSH key authentication enforced; password login disabled
- Regular updates for PostgreSQL and system packages applied

These steps ensure that even if the database is secure internally, its underlying environment remains hardened.

| Check | Description |
|-------|--------------|
| ✅ `listen_addresses='localhost'` | Prevents external exposure |
| ✅ `scram-sha-256` | Modern password authentication |
| ✅ TLS enabled | Encrypts data in transit |
| ✅ Least-privilege roles | Isolates access scope |
| ✅ Parameterized queries | Prevents SQL injection |
| ✅ RLS active | Enforces tenant data isolation |
| ✅ Logging active | Enables visibility and auditing |
| ✅ Backups tested | Confirms disaster recovery capability |

This PostgreSQL setup follows a layered defense strategy: restrict access at the network and role level, enforce modern authentication (SCRAM-SHA-256) and encryption (TLS), apply least privilege through role and schema management, use parameterized queries for injection prevention, enable observability with query and connection logging, and maintain tested backups for recovery assurance. Together, these measures create a resilient foundation against common attack vectors like SQL injection, credential theft, and privilege escalation while remaining lightweight enough for a personal development lab.
