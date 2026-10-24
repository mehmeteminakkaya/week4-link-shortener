# Review: Click counter (stage 3, read-only)

Verdict: **REVISE** (two small findings, no functional bugs)

Checked and fine
- Counting happens only on a successful redirect; the 404 path raises before commit.
- `/stats/{code}` (two segments) does not collide with `/{code}` (one segment).
- Existing `links.db` is upgraded in place (`['id','code','url']` -> adds `clicks`).
- Concurrency claim verified: 100 requests from 20 threads -> 100 x 307, `clicks == 100`.

Findings
1. `test_failed_redirect_is_not_counted` is misleadingly named. An unknown code has no
   row, so "not counted" cannot be observed; it only asserts that both routes return 404.
2. `.claude/rules/testing.md` says not to touch the database in tests, but the migration
   test builds a temporary old-schema DB via `monkeypatch`. The rule should say that is
   the one allowed exception, otherwise the guidance contradicts the code.

Out of scope, noted only
- `encode(row_id)` makes codes sequential and guessable (pre-existing starter design).
