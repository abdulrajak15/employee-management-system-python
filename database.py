"""
database.py — Database Utility Module
Cognetix Technology Internship | Level 2 — Project 1
Handles all SQLite connection and query operations.
"""

import sqlite3

DB_FILE = "employees.db"


# ─────────────────────────────────────────────
#  CONNECTION
# ─────────────────────────────────────────────
def create_connection():
    """Create and return a SQLite database connection."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row   # allows dict-like row access
        return conn
    except sqlite3.Error as e:
        print(f"  [DB ERROR] Connection failed: {e}")
        return None


# ─────────────────────────────────────────────
#  TABLE SETUP
# ─────────────────────────────────────────────
def create_table():
    """Create the employees table if it does not exist."""
    conn = create_connection()
    if not conn:
        return
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id     INTEGER PRIMARY KEY,
                name       TEXT    NOT NULL,
                email      TEXT    NOT NULL UNIQUE,
                department TEXT    NOT NULL,
                salary     REAL    NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"  [DB ERROR] Table creation failed: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────
#  QUERY HELPERS
# ─────────────────────────────────────────────
def execute_query(sql: str, params: tuple = ()):
    """Execute INSERT / UPDATE / DELETE queries."""
    conn = create_connection()
    if not conn:
        return False
    try:
        conn.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"  [DB ERROR] Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"  [DB ERROR] Query failed: {e}")
        return False
    finally:
        conn.close()


def fetch_all(sql: str, params: tuple = ()):
    """Execute SELECT query and return all rows."""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.execute(sql, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"  [DB ERROR] Fetch failed: {e}")
        return []
    finally:
        conn.close()


def fetch_one(sql: str, params: tuple = ()):
    """Execute SELECT query and return a single row."""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.execute(sql, params)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"  [DB ERROR] Fetch failed: {e}")
        return None
    finally:
        conn.close()
