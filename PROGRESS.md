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

## Day 2 — DONE (2026-10-24 → 2026-10-27)

Day 2 turned into the PDF-reading work planned for Day 3. The LLM Router (planned Day 2) moves to Day 3.

Built:
- Added Gemini (`google-genai`) + `python-dotenv` + `docling` to the project
- First Gemini call works (one prompt in, one answer out) — `gemini-3.1-flash-lite`, key read from `.env`
- `scripts/peek_raw.py` — turns the 5 lease PDFs into text with Docling (output in `scratch/`, not committed)
- `scripts/peek_items.py` — shows how Docling labels each piece of text and which page it is on
- `src/clauselens/schemas/clause.py` — `Block_format` (one piece of text + page) and `Clause_format` (number, title, text, page)
- `src/clauselens/ingest/parser.py` — `parse_pdf()` turns a PDF into blocks with page numbers; `clean_text()` fixes ₹ and `\_`; `normalize()` evens out spaces and curly quotes so text can be compared (used only for comparing, never changes what is shown)
- `src/clauselens/ingest/chunker.py` — `groupBlocks_toClauses()` groups blocks into clauses at each heading; text before the first heading becomes "Preamble"; a clause keeps the page it starts on
- `scripts/realPass_chunker.py` — runs the chunker on leases 02–05 and checks the clause count
- Tests: `tests/unit/test_parser.py` (parser + 9 `normalize()` cases; renamed from `test_ingest.py`) + `tests/unit/test_chunker.py` (numbered heading, heading without number, clause over two pages)

Test results: 27 passed. Real PDFs: lease_02 = 17, lease_03 = 18, lease_04 = 17, lease_05 = 18 clauses — all match.

Found:
- Docling reads the leases cleanly: headings, clause numbers and paragraphs all come through
- ₹ came out as "n" (e.g. "n32,000") → fixed in `clean_text()`
- Sub-clause numbers like "4.2" are stored as clause 4 (only the first number is kept)

Cleaned up:
- `src/clauselens/schemas/1.py` deleted
- `scratch/` removed from git (files stay on disk) and ignored; `.DS_Store` ignored too

Build days used: 2 of 13

## Day 3 — IN PROGRESS (2026-10-28 → ): LLM Router (moved from Day 2)

Built so far:
- `src/clauselens/config.py` — `Settings` reads the Gemini key and options from `.env` (pydantic-settings): main model `gemini-3.1-flash-lite`, backup model `gemini-3.5-flash-lite`, retry count and wait times, request timeout, cache folder. `get_settings()` loads them once and reuses them
- `src/clauselens/llm/router.py`:
  - `LLMResult` — what we keep from each call: text, model, input / output / thinking tokens, time taken
  - `make_client()` — Gemini client with a timeout; the SDK's own retries are turned off so ours are the only ones
  - `call_gemini()` — one call; an empty answer counts as an error, not a success
  - `call_with_retry()` — retries temporary errors (429, 500, 503, 504), waiting 2, 4, 8… seconds (max 60), up to 4 retries
  - `call_with_fallback()` — tries the main model first; if it still fails after retries, or the model name is wrong (404), tries the backup model
- `scripts/try_router.py` — manual check: backup model on its own, normal call, and a forced switch to the backup using a fake model name

Test results: 27 passed (no automatic tests for the router yet)

Still to do for Day 3:
- Save answers so the same question is not paid for twice (`cache_dir` setting is ready, not used yet)
- Cost log for every call
- Unit tests for the router with a fake Gemini (no real API calls)
- Check lease_01 clause count (carried from Day 2)

Found:
- `pydantic-settings` is used in `config.py` but isn't listed in `pyproject.toml`; it only works because Docling installs it → add it with `uv add pydantic-settings`
- A 404 (wrong model name) never gets better with retries, so it goes straight to the backup model
