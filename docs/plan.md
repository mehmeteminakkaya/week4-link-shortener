# Plan: Click counter (stage 1, read-only)

Behavior
- `GET /stats/{code}` -> 200 `{"url": ..., "clicks": N}`; unknown code -> 404.
- Only a successful `GET /{code}` redirect increments clicks. Stats calls and 404s do not.

Files: `main.py` (schema + stats route + counting in `redirect`), `test_main.py`.

Findings that shaped the plan
1. Existing `links.db` has columns `[id, code, url]`. `CREATE TABLE IF NOT EXISTS`
   will not add `clicks`, so `init_db()` must check `PRAGMA table_info(links)` and
   `ALTER TABLE ... ADD COLUMN clicks INTEGER NOT NULL DEFAULT 0`.
2. `/stats/{code}` has two path segments, `/{code}` has one: no route conflict.
3. Increment with one `UPDATE ... SET clicks = clicks + 1 WHERE code = ?` (no
   read-modify-write race) and use `rowcount == 0` to detect the 404 case.
4. Tests must not assume specific codes or a clean DB (shared `links.db`).
