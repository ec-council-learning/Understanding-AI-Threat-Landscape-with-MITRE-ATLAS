"""
FIXED version of vulnerable_login.py -- the mitigations for Demo B.
"""
import os


def find_user(db, username):
    cur = db.cursor()
    # FIX 1: parameterized query -- the driver binds the value, no string injection.
    return cur.execute("SELECT id, role FROM users WHERE name = ?", (username,)).fetchone()


def acquire_singleton_lock(path):
    # FIX 2: atomic create -- O_CREAT | O_EXCL makes "check and create" one
    # indivisible syscall, so there is no TOCTOU window to race.
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as f:
        f.write(str(os.getpid()))
    return True
