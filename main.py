#!/usr/bin/env python3
"""
===============================================================================
Database Security Configuration Checker (MySQL) - CAAT Framework
===============================================================================
Role: Senior Data Engineer & IT Audit Manager
Context: IT Audit Portfolio Project
Purpose: Orchestrates modular database security auditing, extracts security 
         anomalies from mysql.user, exports audit_findings.csv, and dynamically 
         generates the AUDIT_EVIDENCE.md proof of execution.
===============================================================================
"""

from audit_engine import (
    DB_CONFIG,
    OUTPUT_CSV_FILE,
    EVIDENCE_MD_FILE,
    get_db_connection,
    run_all_checks,
    export_to_csv,
    generate_audit_evidence_md,
    print_terminal_summary,
)


def run_security_audit() -> None:
    """Main execution orchestrator for the database security audit engine."""
    print("Starting Database Security Data Extraction...")
    connection = get_db_connection(DB_CONFIG)

    try:
        # Step 1: Extract security anomalies across all modular ITGC check algorithms
        findings = run_all_checks(connection)

        # Step 2: Export findings to CSV exception report (Audit Working Papers)
        export_to_csv(findings, OUTPUT_CSV_FILE)

        # Step 3: Automatically generate AUDIT_EVIDENCE.md proof of execution
        generate_audit_evidence_md(findings, EVIDENCE_MD_FILE)

        # Step 4: Render completion metrics to terminal
        print_terminal_summary(findings, OUTPUT_CSV_FILE, EVIDENCE_MD_FILE)

    finally:
        connection.close()


if __name__ == "__main__":
    run_security_audit()
