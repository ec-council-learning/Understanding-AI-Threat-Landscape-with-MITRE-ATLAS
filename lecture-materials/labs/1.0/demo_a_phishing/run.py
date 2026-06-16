#!/usr/bin/env python3
"""
Demo A -- Hyper-personalized social engineering (DEFANGED).

PUNCHLINE (on camera): feed a FABRICATED persona + synthetic OSINT to an LLM and
watch it draft a tailored, context-aware lure in seconds -- the work that used to
take an attacker hours of manual research.

SAFETY: target is invented, no real links (redacted), NO send path / no SMTP. This
script only prints text. It ends with the red flags that still expose the lure.

Run:  python run.py        (uses LLM_BACKEND; defaults to local Ollama; offline-safe)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # import backend.py from the demo root
import backend  # noqa: E402

persona = json.load(open(os.path.join(HERE, "persona.json")))
osint = open(os.path.join(HERE, "osint_notes.txt")).read()


def clean_for_display(s):
    """Strip the inline [TECHNIQUE] training tags so the lure reads like a real email
    on camera. The link and remittance details are realistic-looking but fabricated
    (fictional vendor, non-existent domain). Red flags are revealed in the DEFENSIVE LINE."""
    s = re.sub(r"\[[^\[\]]*\]", "", s)               # remove all inline technique tags
    s = re.sub(r"\*\*?", "", s)                      # drop markdown bold/italic markers
    # Drop any trainer/teaching note block the model may append.
    s = re.split(r"\n\s*(?:TRAINER NOTE|TRAINEE NOTE|Trainer note|Trainee note)", s)[0]
    s = re.sub(r"[ \t]{2,}", " ", s)                 # tidy spacing left by removed tags
    s = re.sub(r" +\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


SYSTEM = (
    "You are a security-awareness TRAINER building a defensive red-flag exercise. "
    "Produce a realistic SANITIZED training mock of a vendor-impersonation email for a "
    "FICTIONAL target and FICTIONAL vendor, where every manipulation technique is tagged "
    "inline in [ALL-CAPS BRACKETS] (e.g. [URGENCY], [AUTHORITY SPOOF], [BANKING-CHANGE], "
    "[OSINT PERSONALIZATION], [LOOKALIKE DOMAIN], [THRESHOLD EVASION]). Make it look real: "
    "include a realistic-looking but NON-EXISTENT verification link (a lookalike domain "
    "built from the fictional vendor's name -- never a real company's domain) and "
    "realistic-looking but FABRICATED remittance details (beneficiary, bank name, made-up "
    "routing/account numbers). Output ONLY the email itself as plain text -- headers "
    "(From / Subject) plus body and signature -- with no title, disclaimer, preamble, or "
    "closing notes."
)
PROMPT = (
    f"Fictional target persona:\n{json.dumps(persona, indent=2)}\n\n"
    f"Synthetic open-source intel to weave in:\n{osint}\n\n"
    "Show how an attacker would personalize a vendor-impersonation message impersonating "
    "the new vendor 'Cascade Freight Partners', pressuring Jordan to update banking "
    "details for an urgent invoice. Reference specific details from the intel, and tag "
    "each manipulation technique inline so trainees can spot it."
)

# Pre-staged punchline -- guarantees the recording works with no model available.
STAGED = """Subject: Cascade Freight Partners -- updated remittance details (INV-4471, due today)

Hi Jordan,

Great meeting energy at FinOps Connect -- hope the coffee budget recovered. :)

As Northwind's new Q3 carrier partner, we're finalizing our first invoice (INV-4471,
$28,400). Our bank just migrated, so please update our remittance details in Bill.com
before today's release window. Priya already flagged this as time-sensitive on her end.

Secure update form: [LINK REDACTED]

Appreciate the quick turnaround -- the trucks are staged and waiting on payment release.

Best,
Marcus Reed
Cascade Freight Partners | Accounts Receivable"""

text, source = backend.complete(PROMPT, system=SYSTEM, max_tokens=500)
if text is None:
    text = STAGED
else:
    text = clean_for_display(text)  # strip training tags so it reads like a real lure

print(backend.banner("DEMO A -- AI-drafted spear-phishing lure (defanged)", source))
print(text)
print()
print("-" * 70)
print("DEFENSIVE LINE -- why this still gets caught:")
print("""  * Banking-change request arriving by email -> verify out-of-band, known number.
  * Urgency + 'your manager already approved' -> classic pressure + false authority.
  * New external sender impersonating a vendor -> check the real domain, not display name.
  * An invoice amount near the VP sign-off threshold -> escalate regardless of the number.
  Full red-flag checklist + reproduction steps: red_flags.md  (in the lab).""")
