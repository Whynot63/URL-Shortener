import psycopg2
import base62
import os

DATABASE_URL = os.environ["DATABASE_URL"]

URLS_DB = "short_urls.db"


def create_db():
    with psycopg2.connect(DSN) as conn:
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS urls (id INTEGER NOT NULL PRIMARY KEY, url TEXT)"
        )


def get_short_url(url):
    with psycopg2.connect(DSN) as conn:
        c = conn.cursor()
        id_ = c.execute("SELECT id FROM urls WHERE url=?", (url,)).fetchone()
    if id_:
        id_ = base62.encode(id_[0])
    return id_


def get_full_url(url):
    try:
        id_ = base62.decode(url)
    except ValueError:
        return

    with psycopg2.connect(DSN) as conn:
        c = conn.cursor()
        url = c.execute("SELECT url FROM urls WHERE id=?", (id_,)).fetchone()
    if url:
        return url[0]


def create_short_url(url):
    short_url = get_short_url(url)
    if short_url:
        return short_url

    with psycopg2.connect(DSN) as conn:
        c = conn.cursor()
        num_of_urls = c.execute("SELECT COUNT(*) FROM urls").fetchone()[0]
        c.execute("INSERT INTO urls (id, url) VALUES(?, ?);", (num_of_urls, url))

    return get_short_url(url)


if __name__ == "__main__":
    create_db()
    assert get_full_url("https://www.sqlitetutorial.net/sqlite-insert/") is None
    short_url = create_short_url("https://www.sqlitetutorial.net/sqlite-insert/")
    assert get_full_url(short_url) == "https://www.sqlitetutorial.net/sqlite-insert/"
