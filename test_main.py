from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shorten_and_redirect():
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200
    code = r.json()["code"]
    assert code
    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://example.com"


def test_rejects_bad_url():
    r = client.post("/shorten", json={"url": "ftp://nope"})
    assert r.status_code == 400


def test_unknown_code_404():
    r = client.get("/does-not-exist", follow_redirects=False)
    assert r.status_code == 404


# --- Click counter: GET /stats/{code} ---


def _new_code(url="https://example.com/stats"):
    return client.post("/shorten", json={"url": url}).json()["code"]


def test_stats_starts_at_zero():
    code = _new_code("https://example.com/zero")
    r = client.get(f"/stats/{code}")
    assert r.status_code == 200
    assert r.json() == {"url": "https://example.com/zero", "clicks": 0}


def test_stats_counts_each_redirect():
    code = _new_code()
    for _ in range(2):
        assert client.get(f"/{code}", follow_redirects=False).status_code == 307
    assert client.get(f"/stats/{code}").json()["clicks"] == 2


def test_stats_are_per_link():
    clicked, untouched = _new_code(), _new_code()
    client.get(f"/{clicked}", follow_redirects=False)
    assert client.get(f"/stats/{clicked}").json()["clicks"] == 1
    assert client.get(f"/stats/{untouched}").json()["clicks"] == 0


def test_viewing_stats_does_not_count_as_a_click():
    code = _new_code()
    client.get(f"/stats/{code}")
    client.get(f"/stats/{code}")
    assert client.get(f"/stats/{code}").json()["clicks"] == 0


def test_stats_unknown_code_404():
    r = client.get("/stats/does-not-exist")
    assert r.status_code == 404


def test_unknown_code_is_404_for_both_redirect_and_stats():
    assert client.get("/missing-code", follow_redirects=False).status_code == 404
    assert client.get("/stats/missing-code").status_code == 404


def test_old_database_without_clicks_column_is_upgraded(tmp_path, monkeypatch):
    import sqlite3

    import main

    old_db = tmp_path / "old.db"
    with sqlite3.connect(old_db) as conn:
        conn.execute("CREATE TABLE links (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, url TEXT NOT NULL)")
        conn.execute("INSERT INTO links (code, url) VALUES ('old', 'https://example.com/old')")
    monkeypatch.setattr(main, "DB_PATH", old_db)
    main.init_db()
    r = client.get("/stats/old")
    assert r.status_code == 200
    assert r.json() == {"url": "https://example.com/old", "clicks": 0}
