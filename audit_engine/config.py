"""
audit_engine/config.py
Configuration parameters, credentials dictionary, and system account baselines.
"""
import os
from typing import Dict, Any, Tuple

# Database connection configuration dictionary
DB_CONFIG: Dict[str, Any] = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "YOUR_PASSWORD_HERE"),
    "database": os.environ.get("MYSQL_DATABASE", "mysql"),
    "connection_timeout": 5,
}

OUTPUT_CSV_FILE: str = "audit_findings.csv"
EVIDENCE_MD_FILE: str = "AUDIT_EVIDENCE.md"

# System maintenance accounts excluded from non-administrative outlier analysis
IGNORED_USERS: Tuple[str, ...] = ("root", "mysql.session", "mysql.sys", "mysql.infoschema")
