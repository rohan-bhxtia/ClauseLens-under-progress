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
- `src/clauselens/ingest/parser.py` — `parse_pdf()` turns a PDF into blocks with page numbers; `clean_text()` fixes ₹ and `\_`
- `src/clauselens/ingest/chunker.py` — `groupBlocks_toClauses()` groups blocks into clauses at each heading; text before the first heading becomes "Preamble"; a clause keeps the page it starts on
- `scripts/realPass_chunker.py` — runs the chunker on leases 02–05 and checks the clause count
- Tests: `tests/unit/test_ingest.py` (parser) + `tests/unit/test_chunker.py` (numbered heading, heading without number, clause over two pages)

Test results: 18 passed. Real PDFs: lease_02 = 17, lease_03 = 18, lease_04 = 17, lease_05 = 18 clauses — all match.

Found:
- Docling reads the leases cleanly: headings, clause numbers and paragraphs all come through
- ₹ came out as "n" (e.g. "n32,000") → fixed in `clean_text()`
- Sub-clause numbers like "4.2" are stored as clause 4 (only the first number is kept)

Cleaned up:
- `src/clauselens/schemas/1.py` deleted
- `scratch/` removed from git (files stay on disk) and ignored; `.DS_Store` ignored too

Build days used: 2 of 13

## Day 3 — next: LLM Router (moved from Day 2)

- Retry when Gemini fails
- Backup model when the main one is down
- Save answers so the same question is not paid for twice
- Cost log for every call
- Day 3's PDF + clause work is mostly done; check lease_01 clause count too
