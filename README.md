# SQL Security Lab

This repository is a personal project created to study SQL security practices using PostgreSQL and Python (Flask).  
It is not a tutorial or production-ready application. The purpose of this project is to document what I built and learned while exploring SQL injection, secure query patterns, and database hardening.

## Overview

The project includes two Flask applications and supporting database scripts that I used to experiment with SQL security concepts:

- **vulnerable_app.py** – An intentionally insecure application that demonstrates how SQL injection can occur when queries are not parameterized.  
- **secure_app.py** – A hardened version that uses parameterized queries, proper role permissions, and session-based tenant isolation patterns.

Supporting files include:
- `app/config.py` – Database configuration and environment variable loading.
- `app/db.py` – Connection management with SSL and parameterized query helpers.
- `app/seed.py` – Script for creating schema and seeding data.
- `database/` – SQL files for database schema, seed data, and privilege setup.
- `scripts/` – Utilities for starting PostgreSQL and initializing data.

## Purpose

This project was created to strengthen my understanding of:

- PostgreSQL security features such as authentication methods, role-based access control, and SSL configuration.
- The difference between unsafe query construction and parameterized SQL execution.
- Row-Level Security (RLS) and how tenant isolation can be implemented in application logic.
- How to detect and mitigate SQL injection vulnerabilities through query parameterization and least-privilege database design.

## Key Features

- Demonstrates both insecure and secure query approaches using Flask and psycopg2.
- Implements separate roles and privileges for reading and writing data.
- Includes an optional Row-Level Security (RLS) example using session-level tenant variables.
- Uses SCRAM-SHA-256 for password authentication and enforces SSL mode.
- Includes examples of query performance analysis using `EXPLAIN ANALYZE` and indexing.

## What I Learned

- SQL injection is easy to create unintentionally if user input is concatenated directly into SQL strings.
- Parameterized queries completely neutralize SQL injection attempts when implemented correctly.
- Using distinct database roles for applications enforces the principle of least privilege and limits damage from potential compromise.
- Row-Level Security is a powerful tool for data isolation but requires careful privilege configuration to avoid bypasses.
- Logging and query analysis tools such as `pg_stat_statements` are essential for monitoring database security and performance.


## Notes

- The vulnerable application is intentionally insecure and should never be deployed to any public environment.
- All development and testing for this project were conducted in an isolated lab (VM / Codespace).
- This repository exists as a personal learning artifact and portfolio piece, not a reusable codebase or tutorial.

## License

This project is released under the MIT License.  
See the `LICENSE` file for details.
