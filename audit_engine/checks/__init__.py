"""
audit_engine/checks package aggregator.
Coordinates the execution of all 4 ITGC security anomaly extraction modules.
"""
from typing import List, Dict, Any

from .privileges import check_excessive_privileges
from .network import check_wildcard_network_exposure
from .authentication import check_empty_passwords
from .lifecycle import check_anonymous_accounts


def run_all_checks(connection: Any) -> List[Dict[str, str]]:
    """Execute all modular extraction checks and return aggregated security anomalies."""
    findings: List[Dict[str, str]] = []
    findings.extend(check_excessive_privileges(connection))
    findings.extend(check_wildcard_network_exposure(connection))
    findings.extend(check_empty_passwords(connection))
    findings.extend(check_anonymous_accounts(connection))
    return findings


__all__ = [
    "run_all_checks",
    "check_excessive_privileges",
    "check_wildcard_network_exposure",
    "check_empty_passwords",
    "check_anonymous_accounts",
]
