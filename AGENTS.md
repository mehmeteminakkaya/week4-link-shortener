# AGENTS.md

A tiny URL shortener: FastAPI + SQLite, one app file. Keep it small.

## What it does
- `POST /shorten` with `{"url": ...}` stores the URL and returns `{"code", "short_url"}`.
  Only `http://` and `https://` URLs are accepted (400 otherwise).
- `GET /{code}` redirects (307) to the stored URL; unknown code returns 404.
- The code is the row id encoded in base62 (`encode()` in `main.py`).

## Where things are
- `main.py` — the whole app: DB helpers, `encode()`, request model, both routes.
- `test_main.py` — pytest suite using FastAPI `TestClient` against the real app.
- `docs/TASKS.md` — candidate features (pick one at a time).
- `links.db` — SQLite file created next to `main.py` on import. Gitignored; never commit it.
- `.claude/rules/`, `.claude/skills/` — scoped test rules and the `add-feature` workflow.

## Setup, run, test
```bash
pip install -r requirements.txt
pytest                         # run before and after every change
uvicorn main:app --reload      # http://localhost:8000, docs at /docs
```

## Product boundaries
In scope: creating short links, redirecting, and small per-link data
(alias, click count, expiry) with its own validation and error codes.
Out of scope: users or auth, a web UI, analytics dashboards, other databases,
background jobs, new dependencies. If a task seems to need one of these, stop and ask.

## Conventions
- Use `get_db()` inside `with closing(...)`; use `?` placeholders, never string-built SQL.
- Raise `HTTPException` with the right status code; don't return error dicts.
- `CREATE TABLE IF NOT EXISTS` does not alter an existing table. A schema change must
  also upgrade an existing `links.db` (check `PRAGMA table_info`) or old databases break.
- Keep everything in `main.py` unless a task clearly needs a second module.

## Change workflow
1. **Understand** — read `main.py`, `test_main.py`, and the task text.
2. **Test** — write a failing test for the new behavior (success plus a failure case).
3. **Implement** — the smallest change that makes it pass.
4. **Verify** — run the full `pytest`; the original 3 tests must still pass.
For a whole feature, use the `add-feature` skill (`.claude/skills/add-feature/SKILL.md`).
