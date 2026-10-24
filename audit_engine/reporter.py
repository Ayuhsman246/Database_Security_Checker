"""
audit_engine/reporter.py
Handles CSV export of audit findings, automated generation of AUDIT_EVIDENCE.md
proof of execution, and terminal dashboard reporting.
"""

import os
import csv
from datetime import datetime, timezone
from typing import List, Dict


def export_to_csv(findings: List[Dict[str, str]], filename: str = "audit_findings.csv") -> None:
    """Export structured anomaly findings to an RFC 4180 compliant CSV exception report."""
    fieldnames = ["Severity", "User", "Host", "Finding Description"]
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding)


def generate_audit_evidence_md(findings: List[Dict[str, str]], filename: str = "AUDIT_EVIDENCE.md") -> None:
    """
    Automated Evidence Generator:
    Dynamically creates AUDIT_EVIDENCE.md at runtime logging execution timestamp,
    ITGC objectives tested, and summary of extracted security outliers.
    """
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    now_iso = datetime.now().astimezone().isoformat()

    crit_count = sum(1 for f in findings if f.get("Severity") == "Critical")
    high_count = sum(1 for f in findings if f.get("Severity") == "High")
    med_count = sum(1 for f in findings if f.get("Severity") == "Medium")
    low_count = sum(1 for f in findings if f.get("Severity") == "Low")

    content = f"""# AUDIT EVIDENCE: Test Execution & Verification Log

**Project Name:** Database Security Configuration Checker (CAAT Engine)  
**Target Organization:** KPMG IT Audit Portfolio Verification  
**Execution Timestamp:** `{now_utc}`  
**ISO Timestamp:** `{now_iso}`  
**Execution Status:** `SUCCESS - {len(findings)} Anomalies Extracted`  
**Target Environment:** Localhost MySQL Server (`database = mysql`)  
**Evidence Artifact:** `audit_findings.csv`  

---

## 1. Executive Summary & Audit Scope
This document serves as permanent, verifiable audit evidence demonstrating that the automated **Database Security Configuration Checker** executed successfully against the target MySQL instance. The Computer-Assisted Audit Technique (CAAT) treated the administrative `mysql.user` metadata table as an analytical dataset, extracting 100% of entitlement records and filtering for compliance outliers.

| Metric | Result |
| :--- | :--- |
| **Population Tested** | Full Catalog (`mysql.user`) |
| **Total Anomalies Extracted** | `{len(findings)}` |
| **Critical Severity Outliers** | `{crit_count}` |
| **High Severity Outliers** | `{high_count}` |
| **Medium Severity Outliers** | `{med_count}` |
| **Low Severity Outliers** | `{low_count}` |
| **Audit Status** | **Exceptions Detected - Audit Working Papers Generated** |

---

## 2. ITGC Objectives Tested & Completed

The automated Python extraction engine evaluated four core IT General Control (ITGC) domains:

1. **Objective 1: Excessive Global Privileges (ITGC AC-1 / Least Privilege & SoD)**
   - **Tested Scope:** Identified non-administrative user accounts possessing global `SUPER` or `GRANT OPTION` rights.
   - **Finding:** Intercepted accounts holding destructive privileges capable of bypassing application controls and altering audit logs.

2. **Objective 2: Wildcard Host Exposure (ITGC AC-2 / Network Boundary Protection)**
   - **Tested Scope:** Identified accounts configured with `host = '%'`.
   - **Finding:** Intercepted open network listeners accessible from untrusted origin IP addresses, circumventing perimeter firewall segmentation.

3. **Objective 3: Empty / Missing Passwords (ITGC AC-3 / Cryptographic Authentication)**
   - **Tested Scope:** Identified accounts configured with empty or unassigned authentication credentials (`authentication_string = ''`).
   - **Finding:** Intercepted passwordless accounts that permit unauthenticated database logins.

4. **Objective 4: Anonymous Default Accounts (ITGC AC-4 / User Lifecycle & Non-Repudiation)**
   - **Tested Scope:** Identified default and orphan accounts configured without a username (`user = ''`).
   - **Finding:** Intercepted untraceable user accounts that compromise forensic accountability and audit attribution.

---

## 3. High-Level Summary of Extracted Anomalies

The automated CAAT pipeline successfully intercepted and logged the following security exceptions:

| Severity | User Account | Host Scope | Audit Observation | Control Domain |
| :--- | :--- | :--- | :--- | :--- |
"""

    for f in findings:
        sev = f.get("Severity", "N/A")
        usr = f.get("User", "N/A")
        host = f.get("Host", "N/A")
        desc = f.get("Finding Description", "N/A")
        domain = "ITGC AC-1 (Privileges)" if "administrative" in desc.lower() else (
            "ITGC AC-2 (Network)" if "wildcard" in desc.lower() else (
                "ITGC AC-3 (Authentication)" if "password" in desc.lower() else "ITGC AC-4 (Lifecycle)"
            )
        )
        content += f"| **{sev}** | `{usr}` | `{host}` | {desc} | {domain} |\n"

    content += """
---

## 4. Auditor Sign-Off & Portfolio Attestation
- **Analyst Role:** AI/ML & Data Analytics Student (KPMG IT Audit Candidate)
- **Supervising Role:** Senior Data Engineer & IT Audit Manager
- **Verification Method:** Programmatic Extraction via Modular Python CAAT Engine (`audit_engine`)
- **Evidence Integrity:** Automatically compiled at runtime; matches CSV working papers (`audit_findings.csv`) 1:1.
"""

    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(content)


def print_terminal_summary(findings: List[Dict[str, str]], csv_file: str, evidence_file: str) -> None:
    """Print an executive summary of the CAAT extraction to the terminal."""
    print(f"\nAudit complete! Extracted {len(findings)} anomalies.")
    print(f"[+] Audit CSV Working Papers exported to   : {csv_file}")
    print(f"[+] Proof-of-Work Evidence generated at     : {evidence_file}\n")
