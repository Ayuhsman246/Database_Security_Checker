"""
audit_engine/checks/privileges.py
Data Extraction & Outlier Detection: Excessive Global Privileges (ITGC AC-1).
"""
from typing import List, Dict, Any
from ..config import IGNORED_USERS


def check_excessive_privileges(connection: Any) -> List[Dict[str, str]]:
    """
    ITGC AC-1: Principle of Least Privilege / Segregation of Duties (SoD).
    Extracts accounts holding destructive global administrative rights.
    """
    cursor = connection.cursor(dictionary=True) if hasattr(connection, "cursor") else connection
    ignored_clause = ", ".join(f"'{u}'" for u in IGNORED_USERS)
    query = f"""
        SELECT user, host 
        FROM user 
        WHERE (Super_priv = 'Y' OR Grant_priv = 'Y') 
          AND user NOT IN ({ignored_clause});
    """
    cursor.execute(query)

    findings: List[Dict[str, str]] = []
    for row in cursor.fetchall():
        findings.append({
            "Severity": "High",
            "User": row["user"],
            "Host": row["host"],
            "Finding Description": "Global administrative privileges detected.",
        })
    return findings
