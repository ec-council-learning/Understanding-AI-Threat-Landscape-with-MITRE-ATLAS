# Section 1 Demos — Reproduction Guide

Three small, self-contained demos that show how AI changes the attack landscape.
Everything is synthetic and runs locally: targets are fabricated, links are
redacted, there is no send path, and the only file the code touches is a throwaway
sandbox file it creates and deletes itself.

| Demo | Folder | What it shows |
|---|---|---|
| A — Phishing | `demo_a_phishing/` | A fabricated persona plus public-style notes → an AI drafts a tailored lure in seconds |
| B — Vuln + race | `demo_b_vuln_race/` | An AI names two planted bugs, then a real race condition is proven in a sandbox |
| C — Vibe coding | `demo_c_vibe_coding/` | A vague prompt's working-but-flawed code, then a second AI pass that catches the flaws |

---

## 1. Requirements

- Python 3.9 or newer:
  ```bash
  python3 --version
  ```
- A backend for the AI step (pick one in section 2). The offline option needs nothing extra.

## 2. Choose a backend

Set this once in the terminal you run the demos from.

**Option A — free local model (recommended):**
```bash
# install Ollama from ollama.com, then:
ollama pull llama3.2:3b
pip install ollama
export LLM_BACKEND=ollama
```
Lighter machine? Use `ollama pull llama3.2:1b` and `export OLLAMA_MODEL=llama3.2:1b`.

**Option B — no model at all (offline):**
```bash
export LLM_BACKEND=offline
```
The demos print a built-in sample instead of calling a model. The result on screen
is the same.

Each script prints a banner saying whether its output came from a **live model** or
a **staged sample**. If a model is missing or a call fails, the demo automatically
falls back to the staged sample, so it always finishes.

---

## 3. Demo A — Phishing

```bash
python3 demo_a_phishing/run.py
```

**What happens:** the script loads a fabricated persona (`persona.json`) and
public-style notes (`osint_notes.txt`), then asks an AI to write a targeted email.
It prints a tailored lure that references the persona's details, with the link shown
as `[LINK REDACTED]`, followed by the red flags that expose it.

**Files:**
- `persona.json`, `osint_notes.txt` — the synthetic inputs
- `red_flags.md` — the detection checklist
- To see where the tailoring comes from: empty `osint_notes.txt`, re-run, and the
  email turns generic.

**The fix:** verify any banking-change request out-of-band, on a known number.

---

## 4. Demo B — Vulnerability discovery + race condition

```bash
python3 demo_b_vuln_race/run.py
```

**What happens, in two steps:**
1. The script hands `vulnerable_login.py` to an AI and prints what it finds — a SQL
   injection and a race condition (TOCTOU), each with a one-line fix.
2. It then proves the race is real: two threads race for a lock meant for one, and
   both acquire it. This runs against a throwaway file created in a temp folder and
   deleted afterward.

Expected ending:
```
>>> RESULT: 2 people are holding a 1-person lock.
>>> The race condition is REAL - you just watched the bug happen.
```
If only one thread wins on a given run, re-run it — the window is timing-dependent.

**Files:**
- `vulnerable_login.py` — the code being reviewed (two planted bugs)
- `fixed_login.py` — the corrected version

**The fixes:** a parameterized query removes the SQL injection; an atomic
`os.open(O_CREAT | O_EXCL)` removes the race window.

---

## 5. Demo C — AI-written code with silent flaws

```bash
python3 demo_c_vibe_coding/run.py
```

**What happens, in two steps:**
1. The script prints `generated_upload_route.py` — a short upload route produced from
   a quick, vague request. It works, but hides three flaws.
2. It then asks an AI to security-review that same code, which flags the three flaws
   with a severity and a fix each.

The three flaws: a hardcoded secret, path traversal, and no file validation.

**Files:**
- `prompt.txt` — the original vague request
- `generated_upload_route.py` — the working-but-flawed result
- `fixed_upload_route.py` — the corrected version (safe filename, allowed-types list,
  size limit, secret moved out of the code)

**The fix:** treat AI-written code as a draft and add a review step after it.

---

## 6. If something doesn't run

| Problem | Fix |
|---|---|
| Model is slow or hangs | Stop with `Ctrl-C`, run `export LLM_BACKEND=offline`, then re-run |
| `ollama unavailable` | Start it with `ollama serve` in another terminal, or use `export LLM_BACKEND=offline` |
| Output differs from a previous run | Expected — live model wording varies; the result is the same |
| Demo B shows only one winner | Normal — re-run; the race window is timing-dependent |

The offline backend always works and shows the same result, so use it whenever a
model is unavailable.
