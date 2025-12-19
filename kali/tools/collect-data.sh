#!/bin/bash
# OPEL - Data Collection Script for Reporting
# Collects and organizes scan data for report generation

set -e

REPORTS_DIR="/root/reports"
SCAN_DIR="${REPORTS_DIR}/scans"
INTEL_DIR="/root/intel"
OUTPUT_DIR="${REPORTS_DIR}/collected_data"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "${OUTPUT_DIR}"

echo "[*] Collecting data for reporting - $(date)"
echo "============================================"

# Create summary file
SUMMARY_FILE="${OUTPUT_DIR}/summary_${TIMESTAMP}.txt"
echo "OPEL Data Collection Summary" > "${SUMMARY_FILE}"
echo "Generated: $(date)" >> "${SUMMARY_FILE}"
echo "================================" >> "${SUMMARY_FILE}"
echo "" >> "${SUMMARY_FILE}"

# Collect scan results
echo "[*] Collecting scan results..."
if [ -d "${SCAN_DIR}" ]; then
    echo "Scan Results:" >> "${SUMMARY_FILE}"
    ls -lh "${SCAN_DIR}" >> "${SUMMARY_FILE}"
    echo "" >> "${SUMMARY_FILE}"
    
    # Copy latest scan files
    cp -r "${SCAN_DIR}"/* "${OUTPUT_DIR}/scans/" 2>/dev/null || mkdir -p "${OUTPUT_DIR}/scans"
fi

# Collect intelligence data
echo "[*] Collecting intelligence data..."
if [ -d "${INTEL_DIR}" ]; then
    echo "Intelligence Data:" >> "${SUMMARY_FILE}"
    find "${INTEL_DIR}" -type f -exec ls -lh {} \; >> "${SUMMARY_FILE}"
    echo "" >> "${SUMMARY_FILE}"
    
    # Copy intelligence data
    cp -r "${INTEL_DIR}"/* "${OUTPUT_DIR}/intel/" 2>/dev/null || mkdir -p "${OUTPUT_DIR}/intel"
fi

# Generate protocol summary
echo "[*] Generating protocol summary..."
PROTOCOL_SUMMARY="${OUTPUT_DIR}/protocols_${TIMESTAMP}.txt"
echo "Detected Protocols:" > "${PROTOCOL_SUMMARY}"
echo "===================" >> "${PROTOCOL_SUMMARY}"
echo "" >> "${PROTOCOL_SUMMARY}"

# Check for protocol evidence in scan files
for protocol in modbus s7 iec104 dnp3 bacnet ethernetip snmp; do
    if find "${SCAN_DIR}" -name "*${protocol}*" -type f | grep -q .; then
        echo "[+] ${protocol^^} - Evidence found" >> "${PROTOCOL_SUMMARY}"
    fi
done

# Generate vulnerability summary
echo "[*] Generating vulnerability summary..."
VULN_SUMMARY="${OUTPUT_DIR}/vulnerabilities_${TIMESTAMP}.txt"
echo "Potential Vulnerabilities:" > "${VULN_SUMMARY}"
echo "===========================" >> "${VULN_SUMMARY}"
echo "" >> "${VULN_SUMMARY}"

# Check for common OT vulnerabilities in scan results
if [ -f "${SCAN_DIR}/nmap_full_${TIMESTAMP}.nmap" ]; then
    grep -i "open\|vulnerable\|weak" "${SCAN_DIR}/nmap_full_${TIMESTAMP}.nmap" >> "${VULN_SUMMARY}" || true
fi

# Create JSON summary for automated processing
JSON_SUMMARY="${OUTPUT_DIR}/summary_${TIMESTAMP}.json"
cat > "${JSON_SUMMARY}" << EOF
{
  "timestamp": "${TIMESTAMP}",
  "scan_directory": "${SCAN_DIR}",
  "intel_directory": "${INTEL_DIR}",
  "protocols_detected": [],
  "vulnerabilities_found": [],
  "files_collected": $(find "${OUTPUT_DIR}" -type f | wc -l)
}
EOF

echo "[+] Data collection completed"
echo "    Output directory: ${OUTPUT_DIR}"
echo "    Summary: ${SUMMARY_FILE}"
ls -lh "${OUTPUT_DIR}"


