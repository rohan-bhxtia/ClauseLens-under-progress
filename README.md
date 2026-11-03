# ClauseLens

**Know what you're signing before you sign it.**

Upload an Indian rental agreement (PDF). ClauseLens extracts key terms (rent, deposit, lock-in, notice period…), shows the exact source quote and page for each answer, and flags risky clauses.

> Informational only. Not legal advice.

## Status

🚧 In progress. **Day 3 of 10 done. Day 4 is next.**

Working so far:
- 15 key lease questions defined, with hand-checked answers for 5 test leases
- PDF reading with page numbers using Docling, including a fix for the corrupted ₹ symbol
- Text normalisation (spaces and curly quotes) for reliable quote matching
- Splitting leases into clauses while preserving clause numbers, titles and starting pages
- Settings loaded from `.env` (API key, models, retry options and cache directory)
- Gemini LLM Router with retry logic and automatic backup-model fallback
- JSON response cache to avoid repeating identical Gemini requests
- Router unit tests using mocked Gemini responses
- Manual integration checks against the real Gemini API

## Next

- Build clause retrieval for the 15 lease questions
- Compare retrieved clauses against verified gold evidence
- Measure retrieval accuracy
- Integrate Gemini structured fact extraction in the following milestone

Day-by-day log: [PROGRESS.md](PROGRESS.md)

## How accuracy is measured

- 5 test leases with 15 hand-checked answers each (`eval/gold/`)
- ClauseLens results will be compared against these verified answers
- Retrieval and extraction accuracy will be measured separately
- Results will be published here once measured. No numbers are claimed before then.

## Run tests

```bash
uv sync
uv run pytest
```
