#!/bin/bash
# OPEL - OT Simulator Startup Script
# Orchestrates all protocol simulators

set -e

CONFIG_DIR="/app/config"
LOG_DIR="/app/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create log directory
mkdir -p "${LOG_DIR}"

echo "=========================================="
echo "OPEL - OT Simulator Starting"
echo "=========================================="
echo "Timestamp: $(date)"
echo ""

# Function to start a service in background
start_service() {
    local name=$1
    local command=$2
    echo "[*] Starting ${name}..."
    eval "${command}" > "${LOG_DIR}/${name}_${TIMESTAMP}.log" 2>&1 &
    local pid=$!
    echo $pid > "/tmp/${name}.pid"
    sleep 3
    # Check if process is still running
    if command -v ps >/dev/null 2>&1; then
        if ps -p $pid > /dev/null 2>&1; then
            echo "  [+] ${name} started (PID: $pid)"
        else
            # Check if there are any errors in the log
            if [ -f "${LOG_DIR}/${name}_${TIMESTAMP}.log" ]; then
                local error_count=$(grep -i "error\|exception\|traceback" "${LOG_DIR}/${name}_${TIMESTAMP}.log" | wc -l)
                if [ "$error_count" -gt 0 ]; then
                    echo "  [!] ${name} failed to start (check ${LOG_DIR}/${name}_${TIMESTAMP}.log)"
                else
                    # Process might have exited quickly, check if it's a simple listener that's working
                    echo "  [*] ${name} process started (may be using fallback mode)"
                fi
            else
                echo "  [!] ${name} failed to start (no log file)"
            fi
        fi
    else
        echo "  [*] ${name} started (PID: $pid, ps not available for verification)"
    fi
}

# Start Modbus simulator
if [ "${MODBUS_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/modbus_server.py" ]; then
        start_service "modbus" "python3 ${CONFIG_DIR}/protocols/modbus_server.py"
    else
        echo "[!] Modbus simulator script not found"
    fi
fi

# Start DNP3 simulator
if [ "${DNP3_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/dnp3_server.py" ]; then
        start_service "dnp3" "python3 ${CONFIG_DIR}/protocols/dnp3_server.py"
    else
        echo "[!] DNP3 simulator script not found"
    fi
fi

# Start BACnet simulator
if [ "${BACNET_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/bacnet_server.py" ]; then
        start_service "bacnet" "python3 ${CONFIG_DIR}/protocols/bacnet_server.py"
    else
        echo "[!] BACnet simulator script not found"
    fi
fi

# Start EtherNet/IP simulator
if [ "${ETHERNETIP_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/ethernetip_server.py" ]; then
        start_service "ethernetip" "python3 ${CONFIG_DIR}/protocols/ethernetip_server.py"
    else
        echo "[!] EtherNet/IP simulator script not found"
    fi
fi

# Start S7 simulator (SNAP7)
if [ "${S7_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/s7_server.py" ]; then
        start_service "s7" "python3 ${CONFIG_DIR}/protocols/s7_server.py"
    else
        echo "[!] S7 simulator script not found"
    fi
fi

# Start IEC 104 simulator
if [ "${IEC104_ENABLED:-true}" = "true" ]; then
    if [ -f "${CONFIG_DIR}/protocols/iec104_server.py" ]; then
        start_service "iec104" "python3 ${CONFIG_DIR}/protocols/iec104_server.py"
    else
        echo "[!] IEC 104 simulator script not found"
    fi
fi

echo ""
echo "=========================================="
echo "OT Simulators Started"
echo "=========================================="
echo "Logs: ${LOG_DIR}"
echo ""
echo "Running services:"
if command -v ps >/dev/null 2>&1; then
    ps aux | grep -E "(modbus|dnp3|bacnet|ethernetip|s7|iec104)" | grep -v grep || echo "No services found"
else
    echo "ps command not available - cannot check running services"
fi
echo ""
echo "Listening ports:"
if command -v netstat >/dev/null 2>&1; then
    netstat -tuln | grep -E "(502|102|2404|20000|47808|2222)" || echo "No matching ports found"
elif command -v ss >/dev/null 2>&1; then
    ss -tuln | grep -E "(502|102|2404|20000|47808|2222)" || echo "No matching ports found"
else
    echo "netstat/ss commands not available - cannot check listening ports"
fi
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running and handle shutdown
trap 'echo "Shutting down..."; kill $(cat /tmp/*.pid) 2>/dev/null; exit' SIGTERM SIGINT

# Wait for all background processes
wait

