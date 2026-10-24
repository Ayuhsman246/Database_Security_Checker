"""
audit_engine/checks/authentication.py
Data Extraction & Outlier Detection: Empty / Missing Passwords (ITGC AC-3).
"""
from typing import List, Dict, Any
from ..config import IGNORED_USERS


def check_empty_passwords(connection: Any) -> List[Dict[str, str]]:
    """
    ITGC AC-3: Identification, Authentication & Password Standards.
    Extracts accounts with unassigned or empty passwords (authentication_string = '').
    """
    cursor = connection.cursor(dictionary=True) if hasattr(connection, "cursor") else connection
    ignored_clause = ", ".join(f"'{u}'" for u in IGNORED_USERS)
    query = f"""
        SELECT user, host 
        FROM user 
        WHERE authentication_string = '' 
          AND user NOT IN ({ignored_clause});
    """
    cursor.execute(query)

    findings: List[Dict[str, str]] = []
    for row in cursor.fetchall():
        findings.append({
            "Severity": "Critical",
            "User": row["user"] if row["user"] else "ANONYMOUS",
            "Host": row["host"],
            "Finding Description": "Account has no password.",
        })
    return findings
