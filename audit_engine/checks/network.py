"""
audit_engine/checks/network.py
Data Extraction & Outlier Detection: Wildcard '%' Network Exposure (ITGC AC-2).
"""
from typing import List, Dict, Any
from ..config import IGNORED_USERS


def check_wildcard_network_exposure(connection: Any) -> List[Dict[str, str]]:
    """
    ITGC AC-2: Network Boundary & Perimeter Access Restrictions.
    Extracts accounts configured to accept connections from any remote IP ('%').
    """
    cursor = connection.cursor(dictionary=True) if hasattr(connection, "cursor") else connection
    ignored_clause = ", ".join(f"'{u}'" for u in IGNORED_USERS)
    query = f"""
        SELECT user, host 
        FROM user 
        WHERE host = '%' 
          AND user NOT IN ({ignored_clause});
    """
    cursor.execute(query)

    findings: List[Dict[str, str]] = []
    for row in cursor.fetchall():
        findings.append({
            "Severity": "Medium",
            "User": row["user"],
            "Host": row["host"],
            "Finding Description": "Account exposed to wildcard '%' IP addresses.",
        })
    return findings
