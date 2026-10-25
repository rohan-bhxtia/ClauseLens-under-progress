# ClauseLens — Progress

Started: 2026-10-19 · Plan: 10 build days + 3 buffer days (counting build days, not calendar days)

## Versions

| Version | Day | What you can do with it |
|---|---|---|
| v0.1 | 1 | 15 questions in code + checked answers (gold) for 5 leases + tests |
| v0.2 | 2 | Talk to Gemini reliably (retry, backup model, saved answers, cost log) |
| v0.3 | 3 | Read a PDF and split it into clauses with page numbers |
| v0.4 | 4 | Find the right clauses for a question (accuracy measured) |
| v0.5 | 5 | AI fills the 15 facts; each checked against the PDF; first accuracy number |
| v0.6 | 6 | Classifier (is this a lease?) + risk checks + human review of unsure answers |
| v0.7 | 7 | Ask questions, get answers with clause citations; backend API |
| v0.8 | 8 | One-command accuracy report; safety tests; hide personal data |
| v0.9 | 9 | Web page + Docker |
| v1.0 | 10 | GitHub-ready: README, diagram, real numbers, demo |
| extra | 11–13 | Catch up first; then compare two leases |

## Day 1 — DONE (2026-10-24)

Built:
- Project set up with uv (pyproject.toml, uv.lock, .gitignore)
- `src/clauselens/schemas/lease.py` — 15 questions + 3 rules (found / not_stated / unclear), written by Rohan
- `eval/gold/lease_01..05.json` — 75 answers, every quoted line verified to exist on its page, reviewed by Rohan
- `tests/test_lease.py` — gold files valid + checker rejects broken data
- First git commit

Test results: all tests passed (run by Rohan on his Mac)

Found:
- ₹ symbol extracts as "■" from these PDFs → handle on Day 3
- Tests caught a real bug: "licence" vs "license" spelling mismatch
- All 5 leases are GPT-made, clean style → add 3–5 real public templates later
- `late_fee` is not_stated in all 5 leases → cannot be scored yet

Decisions:
- Every fact = answer + exact line + page + status
- v1 = leases only; other contract types = new schema file later
- Cut from v1: deposit-deduction reasons list; names/addresses never extracted
- Classifier (doc type) on Day 6 is separate from LLM Router (Day 2)

Build days used: 1 of 13 (took 6 calendar days — mostly learning setup concepts)

## Day 2 — IN PROGRESS (2026-10-24 → 2026-10-25)

Built:
- Added Gemini (`google-genai`) + `python-dotenv` + `docling` to the project
- First Gemini call works (one prompt in, one answer out) — `gemini-3.1-flash-lite`, key read from `.env`
- `scripts/peek_raw.py` — turns the 5 lease PDFs into text with Docling, saves to `scratch/lease_01..05_raw.md`

Found:
- Docling reads the leases cleanly: headings, clause numbers and paragraphs all come through
- ₹ symbol now comes out as "n" (e.g. "n32,000") instead of "■" → still needs fixing on Day 3
- Started on Day 3 work (PDF reading) before finishing Day 2 (LLM Router)

Loose ends:
- `src/clauselens/schemas/1.py` is a scratch test file — it holds a copy of the PDF script (with the wrong path `data/raw/`; PDFs are in `data/`). Adding `1.py` to `.gitignore` does nothing because git already tracks it → delete it, or `git rm --cached` it
- `scratch/` is not in `.gitignore` yet — decide whether to commit the raw text files

Still to do for Day 2 (LLM Router):
- Retry when Gemini fails
- Backup model when the main one is down
- Save answers so the same question is not paid for twice
- Cost log for every call

## Day 3 — next: Read PDF + split into clauses