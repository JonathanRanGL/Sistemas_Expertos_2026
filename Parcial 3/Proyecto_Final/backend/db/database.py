"""
Conexión y utilidades para SQLite — Tienda Inteligente
"""
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "tienda.db"


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a SQLite con row_factory para diccionarios."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Resultados como dict
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Ejecuta un SELECT y devuelve lista de dicts."""
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]


def execute(sql: str, params: tuple = ()) -> int:
    """Ejecuta INSERT/UPDATE/DELETE. Devuelve lastrowid."""
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def execute_many(sql: str, params_list: list[tuple]) -> None:
    """Ejecuta múltiples operaciones en una transacción."""
    with get_connection() as conn:
        conn.executemany(sql, params_list)
        conn.commit()
