# ClauseLens

**Know what you're signing before you sign it.**

Upload an Indian rental agreement (PDF). ClauseLens pulls out the key terms
(rent, deposit, lock-in, notice period…), shows the exact line and page each
answer came from, and flags risky clauses.

> Informational only. Not legal advice.

## Status
🚧 In progress. Day 1 of 10 done.

## How accuracy is measured
- 5 test leases with 15 hand-checked answers each (`eval/gold/`)
- ClauseLens's answers are compared against these to give a score
- Results will be added here once measured. No numbers are claimed before then.

## Run tests
uv sync
uv run pytest