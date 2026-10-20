"""Small helpers for working with SQLite from pandas."""
from __future__ import annotations

import sqlite3

import pandas as pd


def df_to_sqlite(df: pd.DataFrame, table: str, conn: sqlite3.Connection, index: bool = False) -> int:
    """Write a DataFrame to a SQLite table (replacing it) and return the row count."""
    df.to_sql(table, conn, if_exists="replace", index=index)
    return int(conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])


def run_query(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> pd.DataFrame:
    """Run a SELECT with bound parameters (never build SQL by string formatting) and return a DataFrame."""
    return pd.read_sql_query(sql, conn, params=params)


def explain(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[str]:
    """Return SQLite's query plan, one line per step (shows SCAN versus SEARCH)."""
    rows = conn.execute("EXPLAIN QUERY PLAN " + sql, params).fetchall()
    return [r[-1] for r in rows]
