# ClauseLens — Progress

Started: 2026-10-19 · Plan: 10 build days + 3 buffer days

## Versions

| Version | Day | What you can do with it |
|---|---|---|
| v0.1 | 1 | List of 15 facts in code + correct answers for 5 leases written by hand |
| v0.2 | 2 | Talk to Gemini reliably (retry, backup model, saved answers, cost log) |
| v0.3 | 3 | Read a PDF and split it into clauses with page numbers |
| v0.4 | 4 | Find the right clauses for a question (accuracy measured) |
| v0.5 | 5 | AI fills the 15 facts; each checked against the PDF; first accuracy number |
| v0.6 | 6 | Risk checks + pause for human review of unsure answers |
| v0.7 | 7 | Ask questions, get answers with clause citations; backend API |
| v0.8 | 8 | One-command accuracy report; safety tests; hide personal data |
| v0.9 | 9 | Web page + Docker |
| v1.0 | 10 | GitHub-ready: README, diagram, real numbers, demo |
| extra | 11–13 | Catch up first; then compare two leases |

## Day 1 — in progress

Done:
- Defined what ClauseLens does and why
- Got 5 synthetic test leases (GPT-generated, fictional); text extracts fine
- Read lease 1 and 2 together
- Locked the list of 15 facts (cut: deposit deduction reasons → v2; names/addresses → never)

Found:
- ₹ symbol comes out as "■" when extracting text → fix on Day 3
- All 5 leases share one clean GPT style → add 3–5 real public templates

Not done yet:
- Project setup (uv), facts list in Python, hand answers for 5 leases, tests, README

Decisions:
- Every fact = answer + exact line + page + status (found / not stated / unclear)
- Machine: M4 MacBook Air, 16 GB RAM

Days used: 2 of 13 (Day 1 is running into a second day)