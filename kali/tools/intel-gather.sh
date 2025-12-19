#!/bin/bash
# OPEL - Intelligence Gathering Script
# Collects OSINT, threat intelligence, and vulnerability data

set -e

INTEL_DIR="/root/intel"
OSINT_DIR="${INTEL_DIR}/osint"
THREAT_INTEL_DIR="${INTEL_DIR}/threat-intel"
VULN_DB_DIR="${INTEL_DIR}/vuln-db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create directories
mkdir -p "${OSINT_DIR}" "${THREAT_INTEL_DIR}" "${VULN_DB_DIR}"

echo "[*] Starting intelligence gathering - $(date)"
echo "=========================================="

# OSINT Gathering
echo "[*] Gathering OSINT data..."
if command -v theHarvester &> /dev/null; then
    echo "  [*] Running theHarvester..."
    # Example: theHarvester -d example.com -b all -f "${OSINT_DIR}/harvest_${TIMESTAMP}.xml"
fi

# Threat Intelligence Feeds
echo "[*] Checking threat intelligence feeds..."
# ICS-CERT Advisories
curl -s "https://www.cisa.gov/news-events/cybersecurity-advisories" -o "${THREAT_INTEL_DIR}/ics-cert_${TIMESTAMP}.html" || echo "  [!] Failed to fetch ICS-CERT advisories"

# CVE Database queries
echo "[*] Querying CVE database for OT/ICS vulnerabilities..."
# Example CVE search for ICS/SCADA
curl -s "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=SCADA" -o "${VULN_DB_DIR}/cve_scada_${TIMESTAMP}.html" || echo "  [!] Failed to fetch CVE data"

# NIST NVD API (if available)
if [ -n "$NVD_API_KEY" ]; then
    echo "  [*] Querying NIST NVD API..."
    curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=industrial+control+system" \
        -H "apiKey: ${NVD_API_KEY}" \
        -o "${VULN_DB_DIR}/nvd_ics_${TIMESTAMP}.json" || echo "  [!] Failed to query NVD API"
fi

# OT-specific threat intelligence
echo "[*] Gathering OT-specific threat intelligence..."
# Add custom threat intel sources here

echo "[+] Intelligence gathering completed"
echo "    Data stored in: ${INTEL_DIR}"
ls -lh "${INTEL_DIR}"


