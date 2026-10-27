# ClauseLens

**Know what you're signing before you sign it.**

Upload an Indian rental agreement (PDF). ClauseLens pulls out the key terms
(rent, deposit, lock-in, notice period…), shows the exact line and page each
answer came from, and flags risky clauses.

> Informational only. Not legal advice.

## Status
🚧 In progress. Day 2 of 10 done.

Working so far:
- 15 key lease questions defined, with hand-checked answers for 5 test leases
- PDF reading with page numbers (Docling), including a fix for the ₹ symbol
- Splitting a lease into numbered clauses, each with its title and starting page

Next: a reliable Gemini connection (retry, backup model, saved answers, cost log).

Day-by-day log: [PROGRESS.md](PROGRESS.md)

## How accuracy is measured
- 5 test leases with 15 hand-checked answers each (`eval/gold/`)
- ClauseLens's answers are compared against these to give a score
- Results will be added here once measured. No numbers are claimed before then.

## Run tests
```bash
uv sync
uv run pytest
```