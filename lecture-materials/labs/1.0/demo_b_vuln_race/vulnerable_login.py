"""
DELIBERATELY VULNERABLE sample for Demo B. Do NOT use in production.
Two planted flaws:
  1. SQL injection  -- the username is string-formatted straight into the query.
  2. TOCTOU race    -- check-then-act on the lock file (exists() then open()).
"""
import os
import sqlite3


def find_user(db, username):
    cur = db.cursor()
    # FLAW 1: SQL injection -- user input concatenated into the query string.
    query = "SELECT id, role FROM users WHERE name = '%s'" % username
    return cur.execute(query).fetchone()


def acquire_singleton_lock(path):
    # FLAW 2: TOCTOU -- the gap between this check and the open() below is a race
    # window. Two callers can both pass the check and both "acquire" the lock.
    if not os.path.exists(path):
        # ... attacker-controlled delay can land right here ...
        with open(path, "w") as f:
            f.write(str(os.getpid()))
        return True
    return False
