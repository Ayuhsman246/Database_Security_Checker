"""
audit_engine/checks/lifecycle.py
Data Extraction & Outlier Detection: Anonymous Accounts (ITGC AC-4).
"""
from typing import List, Dict, Any


def check_anonymous_accounts(connection: Any) -> List[Dict[str, str]]:
    """
    ITGC AC-4: User Account Lifecycle Hygiene & Identity Governance.
    Extracts anonymous default accounts (user = '') that break audit attribution.
    """
    cursor = connection.cursor(dictionary=True) if hasattr(connection, "cursor") else connection
    query = "SELECT user, host FROM user WHERE user = '';"
    cursor.execute(query)

    findings: List[Dict[str, str]] = []
    for row in cursor.fetchall():
        findings.append({
            "Severity": "High",
            "User": "ANONYMOUS",
            "Host": row["host"],
            "Finding Description": "Anonymous default account detected.",
        })
    return findings
