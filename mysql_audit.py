import mysql.connector
import csv

def run_security_audit():
    print("Starting Database Security Data Extraction...")
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="YOUR_ROOT_PASSWORD", database="mysql")
        cursor = conn.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return

    audit_findings = []
    ignored_users = "('root', 'mysql.session', 'mysql.sys', 'mysql.infoschema')"

    cursor.execute(f"SELECT user, host FROM user WHERE (Super_priv = 'Y' OR Grant_priv = 'Y') AND user NOT IN {ignored_users}")
    for row in cursor.fetchall(): audit_findings.append(["High", row['user'], row['host'], "Global administrative privileges detected."])

    cursor.execute(f"SELECT user, host FROM user WHERE host = '%' AND user NOT IN {ignored_users}")
    for row in cursor.fetchall(): audit_findings.append(["Medium", row['user'], row['host'], "Account exposed to wildcard '%' IP addresses."])

    cursor.execute(f"SELECT user, host FROM user WHERE authentication_string = '' AND user NOT IN {ignored_users}")
    for row in cursor.fetchall(): audit_findings.append(["Critical", row['user'], row['host'], "Account has no password."])

    cursor.execute("SELECT user, host FROM user WHERE user = ''")
    for row in cursor.fetchall(): audit_findings.append(["High", "ANONYMOUS", row['host'], "Anonymous default account detected."])

    with open("audit_findings.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Severity", "User", "Host", "Finding Description"])
        writer.writerows(audit_findings)

    cursor.close()
    conn.close()
    print(f"Audit complete! Extracted {len(audit_findings)} anomalies.")

if __name__ == "__main__":
    run_security_audit()
