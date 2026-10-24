"""
audit_engine/connection.py
Handles MySQL database connection initialization, connection timeout, and teardown.
"""
import sys
from typing import Dict, Any

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception


def get_db_connection(config: Dict[str, Any]) -> Any:
    """Establish and return an authenticated connection to the target MySQL instance."""
    if mysql is None:
        print(
            "[!] Error: Missing required dependency 'mysql-connector-python'.\n"
            "    Please install it using: pip install mysql-connector-python",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        connection = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            connection_timeout=config.get("connection_timeout", 5),
        )
        return connection
    except Error as err:
        print(f"[!] Database Connection Failed: {err}", file=sys.stderr)
        sys.exit(1)
