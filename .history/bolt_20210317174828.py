import sqlite3
from pathlib import Path
from typing import Any, AsyncIterator, Awaitable, Callable, Dict

import aiosqlite
from aiohttp import web
import aiohttp_jinja2
import jinja2

from routes import setup_routes

routes = web.RouteTableDef()


async def init_app() -> web.Application:
    app = web.Application()
    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(
        str('templates')))
    setup_routes(app)
    app.cleanup_ctx.append(init_db)
    return app


async def init_db(app: web.Application) -> AsyncIterator[None]:
    db = await aiosqlite.connect("db.sqlite3")
    app["DB"] = db
    yield
    await db.close()


def get_db_path() -> Path:
    here = Path.cwd()
    while not (here / ".git").exists():
        if here == here.parent:
            raise RuntimeError("Cannot find root github dir")
        here = here.parent

    return here / "db.sqlite3"


def try_make_db() -> None:
    sqlite_db = get_db_path()
    if sqlite_db.exists():
        return

    with sqlite3.connect(sqlite_db) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE logs (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Player_id INTEGER,
            Auction_id INTEGER,
            Desc TEXT,
            Severity TEXT,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        cur.execute(
            """CREATE TABLE players (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Name TEXT,
            Port INTEGER,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        conn.commit()


try_make_db()

web.run_app(init_app())

print("Hello World!")
