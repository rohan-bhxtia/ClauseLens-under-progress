# ClauseLens — Progress

Started: 2026-10-19 · Plan: 10 build days + 3 buffer days (counting build days, not calendar days)

## Versions

| Version | Day | What you can do with it |
|---|---|---|
| v0.1 | 1 | 15 questions in code + checked answers (gold) for 5 leases + tests |
| v0.2 | 2 | Read PDFs and split them into clauses with page numbers |
| v0.3 | 3 | Talk to Gemini reliably (retry, backup model, response cache) |
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

Test results: all tests passed.

Found:
- ₹ symbol extracts incorrectly from some PDFs → handled on Day 2
- Tests caught a real bug: "licence" vs "license" spelling mismatch
- All 5 leases are GPT-made, clean style → add 3–5 real public templates later
- `late_fee` is not_stated in all 5 leases → cannot be scored yet

Decisions:
- Every fact = answer + exact line + page + status
- v1 = leases only; other contract types = new schema file later
- Cut from v1: deposit-deduction reasons list; names/addresses never extracted
- Classifier (doc type) is separate from LLM Router

## Day 2 — DONE (2026-10-24 → 2026-10-27)

Built:
- Added Gemini (`google-genai`), `python-dotenv` and `docling`
- First Gemini API call works — `gemini-3.1-flash-lite`, key read from `.env`
- `scripts/peek_raw.py` — converts lease PDFs into text with Docling
- `scripts/peek_items.py` — inspects Docling labels and page numbers
- `src/clauselens/schemas/clause.py` — `Block_format` and `Clause_format`
- `src/clauselens/ingest/parser.py`:
  - `parse_pdf()` converts PDFs into blocks with page numbers
  - `clean_text()` fixes the corrupted rupee symbol and escaped underscores
  - `normalize()` standardizes whitespace and quotation marks for comparisons only
- `src/clauselens/ingest/chunker.py`:
  - `groupBlocks_toClauses()` groups blocks at headings
  - Text before the first heading becomes "Preamble"
  - Each clause retains its starting page
- `scripts/realPass_chunker.py` — runs the chunker on leases 02–05 and checks clause counts
- Parser and chunker unit tests

Real PDF results:
- lease_02 = 17 clauses
- lease_03 = 18 clauses
- lease_04 = 17 clauses
- lease_05 = 18 clauses
- All matched the expected counts.

Test results: 27 passed.

Found:
- Docling reads headings, clause numbers and paragraphs correctly
- ₹ came out as "n" (e.g. "n32,000") → fixed in `clean_text()`
- Sub-clause identifiers are now preserved as strings (e.g. "2.1", "2.10", "2.1.3")

Cleaned up:
- `src/clauselens/schemas/1.py` deleted
- `scratch/` removed from git and ignored; files remain on disk
- `.DS_Store` ignored

## Day 3 — DONE (2026-10-28 → 2026-11-03): LLM Router

Built:
- `src/clauselens/config.py`:
  - `Settings` reads the Gemini key and options from `.env`
  - Primary model: `gemini-3.1-flash-lite`
  - Backup model: `gemini-3.5-flash-lite`
  - Retry count, wait times, request timeout and cache directory
  - `get_settings()` loads settings once and reuses them
- `src/clauselens/llm/router.py`:
  - `LLMResult` — stores response text, model, input/output/thought tokens and latency
  - `make_client()` — creates the Gemini client with a timeout and disables SDK retries
  - `call_gemini()` — makes one Gemini call and rejects empty responses
  - `call_with_retry()` — checks the cache first, then retries temporary API failures
  - `call_with_fallback()` — tries the primary model and switches to the backup when appropriate
- `src/clauselens/llm/cache.py`:
  - Creates a SHA-256 cache key from the model, prompt and system instruction
  - Saves responses as JSON files
  - Retrieves previously saved responses
- `scripts/try_router.py` — manually checks the backup model, normal primary call and forced fallback
- `tests/unit/test_router.py` — automated router tests using mocked Gemini responses

Test results:
- 34 passed
- 6 deprecation warnings from Docling/Pydantic dependencies
- Router unit tests cover cache hits, cache writes, retries, non-retryable errors and fallback behaviour
- Manual Gemini checks confirmed that both models work and the fallback path is reached

Found:
- SDK retries could multiply our own retries → disabled SDK retries
- A 404 (invalid model name) cannot be fixed by retrying the same model → fallback handles it
- Cache hits avoid repeating identical requests

Decisions:
- Stay on the Gemini free tier
- No pricing configuration or cost logging in the router
- Router remains separate from lease-specific extraction logic
- Router unit tests use mocks; real Gemini calls are checked separately through `scripts/try_router.py`

Build days used: 3 of 13

## Day 4 — NEXT: Clause Retrieval

Goal: Find the most relevant clauses for a given lease question and measure retrieval accuracy.

Planned:
- Define retrieval questions using the existing 15 lease facts
- Build a simple clause retrieval baseline
- Retrieve candidate clauses for each question
- Compare retrieved clauses against the verified gold evidence
- Measure retrieval accuracy before adding more complex retrieval methods

## Day 5 — Structured Fact Extraction

Goal: Use Gemini to extract the 15 lease facts from relevant clauses.

Planned:
- Connect the existing lease schema to the LLM Router
- Send relevant clauses to Gemini
- Extract each fact with its value, exact source quote, page and status
- Validate the response using Pydantic
- Compare extracted facts against the gold answers and calculate the first accuracy score

## Remaining Days

Day 6 — Lease classifier, risk checks and human review.

Day 7 — Question answering with clause citations and backend API.

Day 8 — Accuracy report, safety tests and personal-data protection.

Day 9 — Web page and Docker.

Day 10 — README, architecture diagram, measured results and demo.

Days 11–13 — Buffer, catch-up and lease comparison.

---

**Current milestone:** PDF ingestion and Gemini Router are complete. Next is clause retrieval and its accuracy measurement, followed by structured fact extraction.