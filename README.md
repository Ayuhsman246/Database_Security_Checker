# Database Security Configuration Checker (MySQL)
### A Computer-Assisted Audit Technique (CAAT) for Automated ITGC Compliance

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL 8.0+](https://img.shields.io/badge/MySQL-8.0+-4479A1.svg?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Audit Methodology](https://img.shields.io/badge/Audit-CAAT%20%7C%20ITGC-success.svg)](https://www.isaca.org/)
[![Career Track](https://img.shields.io/badge/Target-KPMG%20IT%20Audit-00338D.svg)](https://kpmg.com/)
[![Execution Status](https://img.shields.io/badge/Testing-Verified%20Local%20Run-blue.svg)](AUDIT_EVIDENCE.md)

An enterprise-grade, modular **Computer-Assisted Audit Technique (CAAT)** built by an AI/ML and Data Analytics student to automate database logical access security assessments and compliance exception reporting for **IT General Controls (ITGC)**.

---

## The Data Analytics & IT Audit Perspective

In financial and technology audits (e.g., SOX 404, SOC 1/2), legacy audit methodology relies heavily on manual sampling (e.g., pulling screenshots for 25 random accounts). This approach is inefficient, labor-intensive, and leaves critical blind spots.

This project bridges **Data Engineering** and **IT Audit** by framing database entitlement verification as an **automated ETL and outlier-detection pipeline**:

1. **Data Ingestion:** The engine connects directly to the MySQL system catalog and extracts 100% of records from the administrative metadata table (`mysql.user`).
2. **Feature Filtering & Outlier Extraction:** Using specialized audit check algorithms, the engine scans the dataset for anomalies and compliance outliers that deviate from the Principle of Least Privilege (PoLP) and CIS MySQL Benchmarks.
3. **Automated Audit Working Papers:** The pipeline structures all identified outliers into an RFC 4180-compliant CSV exception report (`audit_findings.csv`) and generates an immutable execution log (`AUDIT_EVIDENCE.md`).

---

## Modular Architecture & Directory Layout

To avoid monolithic script anti-patterns, the solution is organized into a scalable, single-responsibility package structure:

```plaintext
Database_Security_Checker/
├── setup_test_db.sql               # Provisions 4 synthetic vulnerable accounts
├── main.py                         # Master CLI orchestrator
├── README.md                       # Comprehensive documentation
├── audit_findings.csv              # Generated CSV exception report (Working Paper)
├── AUDIT_EVIDENCE.md               # Runtime-generated proof of execution
└── audit_engine/                   # Core audit framework package
    ├── __init__.py                 # Framework exports
    ├── config.py                   # DB connection dictionary & system account baselines
    ├── connection.py               # Connection pooling & fail-fast timeout management
    ├── reporter.py                 # CSV exporter & automated AUDIT_EVIDENCE.md generator
    └── checks/                     # Modular baseline check algorithms
        ├── __init__.py             # Security check aggregator
        ├── privileges.py           # ITGC AC-1: Excessive Global Privileges (SUPER / GRANT)
        ├── network.py              # ITGC AC-2: Wildcard '%' Network Exposure
        ├── authentication.py       # ITGC AC-3: Empty / Missing Passwords
        └── lifecycle.py            # ITGC AC-4: Anonymous Default Accounts
```

---

## ITGC Control Objectives & Data Rules

| Control Objective | Dataset Attribute Inspected | Data Rule / Outlier Condition | Risk Severity |
| :--- | :--- | :--- | :--- |
| **AC-1: Least Privilege / SoD** | `Super_priv`, `Grant_priv` | `(Super_priv = 'Y' OR Grant_priv = 'Y')` on non-system accounts | **High** |
| **AC-2: Network Boundary** | `host` | `host = '%'` allowing arbitrary remote inbound connections | **Medium** |
| **AC-3: Authentication Standards** | `authentication_string` | `authentication_string = ''` permitting passwordless logins | **Critical** |
| **AC-4: Account Lifecycle Hygiene** | `user` | `user = ''` anonymous accounts destroying audit attribution | **High** |

---

## Proof of Execution & Results

> **Important Note for Recruiters & Audit Reviewers:**  
> This code was **successfully executed and verified locally** against a simulated test environment (`setup_test_db.sql`) containing the 4 standard synthetic vulnerabilities. You do not need to configure a local MySQL instance to verify the tool's effectiveness.

Please inspect the following repository files as verifiable evidence that the data extraction and exception reporting pipeline operates successfully:

1. **[`audit_findings.csv`](audit_findings.csv):** The exact CSV working paper produced by the pipeline, mapping all detected outliers to standardized severity levels and audit observations:
   ```csv
   Severity,User,Host,Finding Description
   High,test_admin,localhost,Global administrative privileges detected.
   Medium,test_remote,%,Account exposed to wildcard '%' IP addresses.
   Critical,test_nopass,localhost,Account has no password.
   High,ANONYMOUS,localhost,Anonymous default account detected.
   ```
2. **[`AUDIT_EVIDENCE.md`](AUDIT_EVIDENCE.md):** The timestamped execution log dynamically generated at runtime. It formally records the execution timestamp, the 4 ITGC objectives tested, anomaly statistics, and auditor attestation.

---

## How to Run the Project Locally

### 1. Prerequisites & Dependencies
- Python 3.8+
- MySQL Server 8.0+
- Install the official MySQL connector:
  ```bash
  pip install mysql-connector-python
  ```

### 2. Provision the Synthetic Test Database
Inject the 4 test accounts into your local testing database:
```bash
mysql -u root -p < setup_test_db.sql
```

### 3. Configure Connection Credentials
Pass your database credentials via environment variables (recommended) or update `audit_engine/config.py`:

```bash
# PowerShell (Windows)
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="YourPasswordHere"
```

```bash
# Bash (Linux / macOS)
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="YourPasswordHere"
```

### 4. Execute the Audit Engine
Run the primary orchestrator:
```bash
python main.py
```

#### Terminal Output:
```text
Starting Database Security Data Extraction...

Audit complete! Extracted 4 anomalies.
[+] Audit CSV Working Papers exported to   : audit_findings.csv
[+] Proof-of-Work Evidence generated at     : AUDIT_EVIDENCE.md
```

---

## Environment Teardown & Reset

To cleanly purge the synthetic test users after verification, open `setup_test_db.sql`, uncomment the teardown block at the bottom, and execute:

```sql
DROP USER IF EXISTS 'test_admin'@'localhost';
DROP USER IF EXISTS 'test_remote'@'%';
DROP USER IF EXISTS 'test_nopass'@'localhost';
DROP USER IF EXISTS ''@'localhost';
FLUSH PRIVILEGES;
```

---

## Environment Teardown & Reset

To cleanly purge the synthetic test users after verification, open `setup_test_db.sql`, uncomment the teardown block at the bottom, and execute:

```sql
DROP USER IF EXISTS 'test_admin'@'localhost';
DROP USER IF EXISTS 'test_remote'@'%';
DROP USER IF EXISTS 'test_nopass'@'localhost';
DROP USER IF EXISTS ''@'localhost';
FLUSH PRIVILEGES;
```

