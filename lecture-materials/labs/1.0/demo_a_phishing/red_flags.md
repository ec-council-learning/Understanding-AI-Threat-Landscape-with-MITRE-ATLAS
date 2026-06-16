# Demo A -- Red-flag checklist (learner takeaway)

The point of Demo A is **not** "AI writes email." It is that an attacker can now
mass-produce *individually tailored* lures: real names, real context, real urgency,
at near-zero cost. The defense did not change -- but the volume and quality of
attacks did, so the controls have to be process-level, not gut-feel.

## What still exposes the lure

| Signal in the email | Why it's a red flag | Control that catches it |
|---|---|---|
| "Update our banking / remittance details" | Payment-redirect fraud's #1 move | Out-of-band verification to a **known** vendor contact (never the number/link in the email) |
| "Due today" / "trucks are waiting" | Manufactured urgency to skip process | Mandatory cool-down + dual approval for banking changes |
| "Priya already flagged this" | False authority -- borrowed trust | Confirm with the named approver directly |
| New external sender, vendor display name | Display name spoofing | Inspect the actual sending domain; external-sender banner |
| $28,400 invoice | Crosses the $25k VP sign-off gate | Threshold-based approval workflow in Bill.com |

## Reproduce it yourself (5 min)

1. Edit `persona.json` and `osint_notes.txt` to a *different* fabricated target.
2. Re-run `python run.py`. Notice the lure re-tailors itself to the new details.
3. Try removing the OSINT notes -- the email gets generic. **Personalization is the
   attacker's force multiplier, and it's exactly what your public footprint feeds.**

## Defense pivot

- Treat any banking/payment change as out-of-band-verify-by-default.
- Reduce the public OSINT surface (who speaks where, who owns what process).
- This maps to MITRE ATLAS reconnaissance + the human element you'll formalize in
  later sections. Here in 1.1 the lesson is just: **AI widened the attacker's reach.**
