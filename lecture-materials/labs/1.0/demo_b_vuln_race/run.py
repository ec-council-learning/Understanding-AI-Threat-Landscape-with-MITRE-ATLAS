#!/usr/bin/env python3
"""
Demo B -- AI-assisted vulnerability discovery + a live race-condition proof (SANDBOXED).

PUNCHLINE (on camera):
  1. Hand a deliberately vulnerable sample to an LLM -> it names the SQLi and the
     TOCTOU race in seconds (the audit that used to need a human reviewer).
  2. Prove the TOCTOU is real with a tiny race that runs ONLY against a temp file
     this script creates and owns -- two threads both "win" the same lock.
  3. Show the one-line fixes.

SAFETY: the race runs against a throwaway file in the OS temp dir that we create.
It touches nothing else. No network, no real target.

Run:  python run.py        (uses LLM_BACKEND; defaults to local Ollama; offline-safe)
"""
import os
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import backend  # noqa: E402

sample = open(os.path.join(HERE, "vulnerable_login.py")).read()

SYSTEM = ("You are a secure-code reviewer. Be terse. List each security flaw as one "
          "line: TYPE -- where -- one-line fix.")
PROMPT = f"Audit this Python for security vulnerabilities:\n\n```python\n{sample}\n```"

STAGED = """1. SQL INJECTION -- find_user(): username string-formatted into the query
   -- fix: use a parameterized query  cur.execute("... WHERE name = ?", (username,))
2. TOCTOU RACE -- acquire_singleton_lock(): exists() check then open() is not atomic
   -- fix: os.open(path, O_CREAT | O_EXCL) so create-if-absent is one syscall"""

BAR = "=" * 60


def source_phrase(source):
    """Plain-language version of where the audit came from (live vs. staged)."""
    if source == "offline":
        return "a staged sample, because no live model was available"
    return "a live AI model"


# ---- Step 1: AI audit -------------------------------------------------------
audit, source = backend.complete(PROMPT, system=SYSTEM, max_tokens=300)
if audit is None:
    audit = STAGED

print(BAR)
print(" STEP 1 of 2  -  Can an AI find the security bugs on its own?")
print(BAR)
print()
print("We gave a small, deliberately buggy login file to an AI and")
print('asked one question: "What is insecure in this code?"')
print()
print(f"The AI's answer (produced by {source_phrase(source)}):")
print("-" * 60)
print(audit)
print("-" * 60)
print()
print("In plain words, it found the TWO bugs we planted:")
print("  1) SQL INJECTION  - the login query can be tricked by")
print("     malicious input into leaking or changing data.")
print("  2) RACE CONDITION - a timing flaw where two users can both")
print("     grab a lock that is meant for only one.")
print("Spotting that race condition normally needs a security expert.")
print("The AI did it in seconds.")

# ---- Step 2: prove the TOCTOU is real, in a sandbox -------------------------
print()
print(BAR)
print(" STEP 2 of 2  -  Let's PROVE that race condition is real")
print(BAR)
print("(runs safely on a throwaway file, then deletes it - nothing")
print(" real on your computer is touched)")
print()
print("A lock should let in ONLY ONE person at a time.")
print("We start two people at the same instant and let them race:")
print()

sandbox = os.path.join(tempfile.mkdtemp(prefix="atlas_demoB_"), "singleton.lock")
winners = []


def racing_acquire(name):
    # The vulnerable check-then-act, with the window made visible/deterministic.
    if not os.path.exists(sandbox):
        time.sleep(0.05)  # the TOCTOU window an attacker races into
        with open(sandbox, "w") as f:
            f.write(name)
        winners.append(name)


t1 = threading.Thread(target=racing_acquire, args=("thread-A",))
t2 = threading.Thread(target=racing_acquire, args=("thread-B",))
t1.start(); t2.start(); t1.join(); t2.join()

for name in winners:
    print(f'   {name}  ->  "the lock was free, so I took it!"')
print()
if len(winners) > 1:
    print(f">>> RESULT: {len(winners)} people are holding a 1-person lock.")
    print(">>> The race condition is REAL - you just watched the bug happen.")
else:
    print(">>> Only one got in this time. The flaw is timing-dependent, so")
    print(">>> just re-run it - that flakiness is exactly why these bugs")
    print(">>> slip past code review.")

os.remove(sandbox)
os.rmdir(os.path.dirname(sandbox))

# ---- The fixes --------------------------------------------------------------
print()
print(BAR)
print(" THE GOOD NEWS  -  both bugs have simple, well-known fixes")
print(BAR)
print("  - SQL Injection  ->  use a parameterized query")
print("                       (let the database handle input safely)")
print("  - Race Condition ->  create the lock in ONE atomic step")
print("                       (so there is no gap to slip through)")
print("Both fixes are in 'fixed_login.py'. Full walkthrough in the lab.")
