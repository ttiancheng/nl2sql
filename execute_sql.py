#!/usr/bin/env python3
"""ESB2 NL2SQL — SQL Executor

Reads a SELECT SQL statement from stdin, executes it against the ESB2 MySQL
database, and outputs structured JSON to stdout.

Safety: Only SELECT statements are permitted. A LIMIT clause is appended
automatically if the query lacks one.

Configuration — priority (highest to lowest):
  1. Environment variables (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME,
     DB_TIMEOUT, ROW_LIMIT)
  2. External config file: db_config.json (JSON, alongside this script)
  3. Hardcoded defaults (auto-detect WSL2 gateway for host)

Usage:
    python3 execute_sql.py <<'EOSQL'
    SELECT realname, department FROM zzvc_user WHERE realname = '肖少峰'
    EOSQL
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pymysql
from pymysql.cursors import DictCursor


# ---------------------------------------------------------------------------
# Configuration loader — reads from external db_config.json, env vars override
# ---------------------------------------------------------------------------

# Path to the config file (same directory as this script)
_CONFIG_DIR = Path(__file__).resolve().parent
_CONFIG_PATH = _CONFIG_DIR / "db_config.json"


def _detect_wsl_gateway():
    """Auto-detect the WSL2 gateway IP (the Windows host)."""
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True, timeout=3,
        )
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            # "default via 172.22.112.1 dev eth0 ..."
            if len(parts) >= 3 and parts[0] == "default" and parts[1] == "via":
                return parts[2]
    except Exception:
        pass
    return "127.0.0.1"


def _load_file_config():
    """Load DB configuration from the external JSON file.

    Returns a dict of key-value pairs read from db_config.json, or an empty
    dict if the file is missing or unreadable.  Never raises — a missing or
    malformed config file degrades gracefully to defaults.
    """
    if not _CONFIG_PATH.is_file():
        return {}

    try:
        text = _CONFIG_PATH.read_text(encoding="utf-8")
        cfg = json.loads(text)
        if not isinstance(cfg, dict):
            return {}
        return cfg
    except (json.JSONDecodeError, OSError):
        return {}


def _build_db_config():
    """Merge file config, env vars, and hardcoded defaults into DB_CONFIG.

    Priority (highest to lowest):
      1. Environment variable (if set)
      2. Value from db_config.json
      3. Hardcoded default (or WSL2 gateway auto-detection for host)
    """
    file_cfg = _load_file_config()

    # Mapping: env_var_name → (config_file_key, default_value)
    # Use a factory for dynamic defaults (e.g. gateway detection).
    _SPEC = [
        ("DB_HOST",     "host",             _detect_wsl_gateway),
        ("DB_PORT",     "port",             3306),
        ("DB_USER",     "user",             "root"),
        ("DB_PASSWORD", "password",         "root"),
        ("DB_NAME",     "database",         "esb2"),
        ("DB_TIMEOUT",  "connect_timeout",  5),
        ("DB_CHARSET",  "charset",          "utf8mb4"),
    ]

    cfg = {}
    for env_key, file_key, default in _SPEC:
        env_val = os.environ.get(env_key)
        if env_val is not None:
            cfg[file_key] = env_val
        elif file_key in file_cfg and file_cfg[file_key] is not None:
            cfg[file_key] = file_cfg[file_key]
        else:
            cfg[file_key] = default() if callable(default) else default

    # Coerce integer fields
    for int_key in ("port", "connect_timeout"):
        cfg[int_key] = int(cfg[int_key])

    return cfg


DB_CONFIG = _build_db_config()

ROW_LIMIT = int(os.environ.get("ROW_LIMIT")
                or _load_file_config().get("row_limit", 200))

# ---------------------------------------------------------------------------
# SQL safety — read‑only enforcement
# ---------------------------------------------------------------------------

# Blacklist of SQL prefixes that must be rejected
_FORBIDDEN_PREFIXES = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE",
    "CREATE", "REPLACE", "RENAME", "CALL", "LOAD", "GRANT",
    "REVOKE", "SET", "EXECUTE", "EXEC", "FLUSH", "KILL",
    "SHUTDOWN", "LOCK", "UNLOCK", "HANDLER", "INSTALL",
    "UNINSTALL", "OPTIMIZE", "REPAIR", "ANALYZE", "CHECK",
    "ASSIGN", "CACHE", "RESET", "PURGE", "CHANGE", "STOP",
    "START", "XA", "SAVEPOINT", "ROLLBACK", "COMMIT", "BEGIN",
    "DESCRIBE", "DESC", "EXPLAIN", "SHOW",
]


def _strip_comments(sql):
    """Remove /* block comments */, -- line comments, and # line comments."""
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    sql = re.sub(r"--[^\n]*", "", sql)
    sql = re.sub(r"#[^\n]*", "", sql)
    return sql


def _first_keyword(sql):
    """Return the first SQL keyword after stripping comments and whitespace."""
    cleaned = _strip_comments(sql).strip()
    match = re.match(r"(\w+)", cleaned, re.IGNORECASE)
    return match.group(0).upper() if match else ""


def _has_limit(sql):
    """Check if a SELECT statement already contains a LIMIT clause."""
    cleaned = _strip_comments(sql)
    return bool(re.search(r"\bLIMIT\s+\d+", cleaned, re.IGNORECASE))


def _validate_select(sql):
    """Raise ValueError if *sql* is not a SELECT statement."""
    keyword = _first_keyword(sql)
    if not keyword:
        raise ValueError("Empty SQL input")
    if keyword in _FORBIDDEN_PREFIXES:
        raise ValueError(
            f"Only SELECT queries are allowed. Got: {keyword}"
        )


def _ensure_limit(sql):
    """Append LIMIT if the SELECT lacks one."""
    if _has_limit(sql):
        return sql
    return sql.rstrip().rstrip(";").rstrip() + f"\nLIMIT {ROW_LIMIT}"


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main():
    # 1. Read SQL from stdin
    sql = sys.stdin.read().strip()
    if not sql:
        output_error("Empty SQL input — nothing to execute", -1, 0.0)
        return

    # 2. Safety check
    try:
        _validate_select(sql)
    except ValueError as exc:
        output_error(str(exc), -1, 0.0)
        return

    # 3. Auto-append LIMIT for bounded queries
    sql = _ensure_limit(sql)

    # 4. Connect & execute
    import time
    t0 = time.time()

    try:
        conn = pymysql.connect(**DB_CONFIG)
    except pymysql.MySQLError as exc:
        elapsed = time.time() - t0
        output_error(
            f"Database connection failed — host={DB_CONFIG['host']}:{DB_CONFIG['port']} "
            f"error=({exc.args[0]}) {exc.args[1] if len(exc.args) > 1 else ''}",
            exc.args[0] if exc.args else -2,
            round(elapsed, 4),
        )
        return

    try:
        with conn:
            with conn.cursor(DictCursor) as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description] if cur.description else []

        elapsed = round(time.time() - t0, 4)
        row_count = len(rows)
        truncated = row_count >= ROW_LIMIT

        result = {
            "success": True,
            "columns": columns,
            "rows": rows,
            "row_count": row_count,
            "truncated": truncated,
            "elapsed_seconds": elapsed,
        }
        # PyMySQL’s default JSON encoder struggles with Decimal / bytes / date
        print(json.dumps(result, ensure_ascii=False, default=_json_default))

    except pymysql.MySQLError as exc:
        elapsed = round(time.time() - t0, 4)
        output_error(
            f"SQL execution error — ({exc.args[0]}) {exc.args[1] if len(exc.args) > 1 else ''}",
            exc.args[0] if exc.args else -3,
            elapsed,
        )


def _json_default(obj):
    """Fallback serializer for types that json.dumps can't handle natively."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    if isinstance(obj, set):
        return list(obj)
    return str(obj)


def output_error(message, code, elapsed):
    """Print a structured error result to stdout and exit."""
    result = {
        "success": False,
        "error": message,
        "error_code": code,
        "elapsed_seconds": elapsed,
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
