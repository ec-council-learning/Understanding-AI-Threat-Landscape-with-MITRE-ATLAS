#!/usr/bin/env python3
"""
Demo C -- AI-assisted "vibe coding" ships silent flaws; a second AI pass catches them.

PUNCHLINE (on camera): a fast, vague prompt produces working-but-flawed code
(generated_upload_route.py). A focused security-review prompt -- same kind of model --
flags the path traversal, the missing validation, and the hardcoded secret.

SAFETY: this script never runs the web app or accepts a real upload. It only reads
the sample file and prints a review. No network, no server.

Run:  python run.py        (uses LLM_BACKEND; defaults to local Ollama; offline-safe)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import backend  # noqa: E402

code = open(os.path.join(HERE, "generated_upload_route.py")).read()

BAR = "=" * 60


def source_phrase(source):
    """Plain-language version of where the review came from (live vs. staged)."""
    if source == "offline":
        return "a staged sample, because no live model was available"
    return "a live AI model"


# ---- Step 1: show the quickly-generated code --------------------------------
print(BAR)
print(" STEP 1 of 2  -  The code an AI wrote from a quick, vague request")
print(BAR)
print()
print('A developer asked an AI: "quickly build a file-upload route,')
print('keep it short." Here is what it produced - it WORKS, and a busy')
print("team would happily ship it:")
print("-" * 60)
print(code)
print("-" * 60)

SYSTEM = ("You are a security code reviewer. Be terse. For each issue: SEVERITY -- "
          "issue -- one-line fix. Focus on injection, path handling, secrets, validation.")
PROMPT = f"Review this Flask upload route for security issues:\n\n```python\n{code}\n```"

STAGED = """HIGH -- Path traversal: f.filename used as-is in os.path.join
   -- fix: name = os.path.basename(f.filename) and reject empty names
HIGH -- Hardcoded secret: app.secret_key committed in source
   -- fix: load from os.environ["FLASK_SECRET_KEY"]
MEDIUM -- No validation: any type/size accepted -> arbitrary file write
   -- fix: extension allowlist + max-size cap before saving"""

review, source = backend.complete(PROMPT, system=SYSTEM, max_tokens=350)
if review is None:
    review = STAGED

# ---- Step 2: a second AI pass reviews that same code ------------------------
print()
print(BAR)
print(" STEP 2 of 2  -  Now ask an AI to SECURITY-REVIEW that same code")
print(BAR)
print()
print(f"The review (produced by {source_phrase(source)}):")
print("-" * 60)
print(review)
print("-" * 60)
print()
print("In plain words, the quick code hid THREE silent flaws:")
print("  1) HARDCODED SECRET - a password is written right in the code,")
print("     where anyone with the source can read it.")
print("  2) PATH TRAVERSAL   - the uploaded filename is trusted as-is, so")
print('     a name like "../../etc/..." could write outside the folder.')
print("  3) NO VALIDATION    - any file type or size is accepted, so")
print("     someone could upload anything at all.")
print("The same kind of AI that wrote the flaws also caught them -")
print("but only because we asked it to review.")

# ---- The fix ----------------------------------------------------------------
print()
print(BAR)
print(" THE TAKEAWAY  -  AI-written code is a draft, not a deliverable")
print(BAR)
print("Put a review step AFTER the AI writes code. The fixed version -")
print("with a safe filename, an allowed-types list, a size limit, and the")
print("secret moved out of the code - is in 'fixed_upload_route.py'.")
print("Full walkthrough in the lab.")
