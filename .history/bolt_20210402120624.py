# Copyright (C) 2021 Anurag Jain
import sqlite3
from pathlib import Path
from typing import AsyncIterator
import os
import aiosqlite
import aiohttp
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
    app.cleanup_ctx.append(init_client)
    return app


def get_db_path() -> Path:
    here = Path.cwd()
    return here / "db.sqlite3"


async def init_db(app: web.Application) -> AsyncIterator[None]:
    db = await aiosqlite.connect("db.sqlite3")
    app["DB"] = db
    yield
    await db.close()
    os.remove(get_db_path())


async def init_client(app: web.Application) -> AsyncIterator[None]:
    client = aiohttp.ClientSession()
    app["client"] = client
    yield
    await client.close()


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
        cur.execute(
            """CREATE TABLE auctions (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Key INTEGER,
            Open INTEGER,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        cur.execute(
            """CREATE TABLE auction_players (
            Auction_id INTEGER,
            Player_id INTEGER,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        cur.execute(
            """CREATE TABLE bids (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Auction_id INTEGER,
            Player_id INTEGER,
            bid_value REAL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        cur.execute(
            """CREATE TABLE transactions (
            Player_id INTEGER,
            value REAL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        conn.commit()


try_make_db()

web.run_app(init_app())
