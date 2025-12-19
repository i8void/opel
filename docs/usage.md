# OPEL Usage Guide

This guide provides detailed instructions for using the OPEL (OT Pentest Lab) environment.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Container Management](#container-management)
3. [Running Scans](#running-scans)
4. [Intelligence Gathering](#intelligence-gathering)
5. [Protocol Testing](#protocol-testing)
6. [Report Generation](#report-generation)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Starting the Lab

```bash
# Build and start all containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the lab
docker-compose down
```

### Accessing Containers

```bash
# Access Kali container
docker exec -it opel-kali /bin/bash

# Access OT simulator container
docker exec -it opel-ot-simulator /bin/bash
```

## Container Management

### Kali Container

The Kali container includes:
- OT-specific scanning tools (Nmap, PLCscan, Modbus-cli)
- Intelligence gathering tools (theHarvester, recon-ng)
- Custom scripts in `/root/tools/`
- Report templates in `/root/reports/`

### OT Simulator Container

The OT simulator container runs:
- Protocol simulators (Modbus, S7, DNP3, BACnet, EtherNet/IP, IEC 104)
- All simulators start automatically on container startup

Check simulator status:
```bash
docker exec opel-ot-simulator ps aux | grep -E "(modbus|dnp3|bacnet|ethernetip|s7|iec104)"
```

## Running Scans

### Basic Network Scan

From the Kali container:
```bash
cd /root/tools
./scan-ot.sh
```

This script performs:
- Comprehensive Nmap scan
- Protocol-specific scans (Modbus, S7, IEC 104, DNP3, BACnet, EtherNet/IP)
- PLCscan enumeration
- Modbus-cli enumeration

### Manual Protocol Scans

#### Modbus TCP (Port 502)
```bash
nmap -p 502 --script modbus-discover,modbus-read-registers ot-simulator
```

#### S7/Siemens (Port 102)
```bash
nmap -p 102 --script s7-info ot-simulator
```

#### IEC 104 (Port 2404)
```bash
nmap -p 2404 -sV ot-simulator
```

#### DNP3 (Port 20000)
```bash
nmap -p 20000 --script dnp3-info ot-simulator
```

#### BACnet/IP (UDP 47808)
```bash
nmap -sU -p 47808 --script bacnet-info ot-simulator
```

#### EtherNet/IP (Port 2222)
```bash
nmap -p 2222 -sV ot-simulator
```

### Using PLCscan

```bash
cd /root/tools/plcscan
python3 plcscan.py ot-simulator
```

### Using Modbus-cli

```bash
# Read holding registers
modbus read ot-simulator 502 1 0 10

# Write to register
modbus write ot-simulator 502 1 0 1234
```

## Intelligence Gathering

### Automated Intelligence Collection

```bash
cd /root/tools
./intel-gather.sh
```

This script collects:
- OSINT data (using theHarvester)
- Threat intelligence feeds
- CVE/vulnerability database queries
- ICS-CERT advisories

### Manual OSINT Gathering

```bash
# Using theHarvester
theHarvester -d example.com -b all -f /root/intel/osint/harvest.xml

# Using recon-ng
recon-ng
```

### Threat Intelligence

Intelligence data is stored in:
- `/root/intel/osint/` - OSINT data
- `/root/intel/threat-intel/` - Threat intelligence feeds
- `/root/intel/vuln-db/` - Vulnerability database queries

## Protocol Testing

### Testing Modbus

```bash
# Using pymodbus (Python)
python3 -c "from pymodbus.client.sync import ModbusTcpClient; client = ModbusTcpClient('ot-simulator'); print(client.read_holding_registers(0, 10))"
```

### Testing S7

```bash
# Using python-snap7
python3 -c "import snap7; client = snap7.client.Client(); client.connect('ot-simulator', 0, 1); print(client.get_cpu_info())"
```

## Report Generation

### Collecting Data for Reports

```bash
cd /root/tools
./collect-data.sh
```

This script:
- Collects all scan results
- Organizes intelligence data
- Generates summaries
- Creates JSON output for automated processing

### Using Report Templates

Report templates are located in `/root/reports/`:
- `engagement-template.md` - Customer engagement report
- `risk-assessment-template.md` - IEC 62443 risk assessment
- `remediation-template.md` - Remediation tracking

To use a template:
1. Copy the template to a new file
2. Fill in the placeholders
3. Include scan results and evidence
4. Export to PDF (using pandoc or similar)

Example:
```bash
cd /root/reports
cp engagement-template.md engagement-client-$(date +%Y%m%d).md
# Edit the file with your findings
```

## Troubleshooting

### Containers Not Starting

```bash
# Check Docker logs
docker-compose logs

# Check container status
docker-compose ps

# Rebuild containers
docker-compose up --build --force-recreate
```

### Simulators Not Responding

```bash
# Check if simulators are running
docker exec opel-ot-simulator ps aux | grep -E "(modbus|dnp3|bacnet|ethernetip|s7|iec104)"

# Check simulator logs
docker exec opel-ot-simulator ls -la /app/logs/

# Restart simulators
docker restart opel-ot-simulator
```

### Network Connectivity Issues

```bash
# Test connectivity from Kali to OT simulator
docker exec opel-kali ping -c 3 ot-simulator

# Check network configuration
docker network inspect opel_opel-lab

# Verify port mappings
docker port opel-ot-simulator
```

### Protocol-Specific Issues

#### BACnet Multicast Not Working
BACnet multicast discovery may not work in Docker bridge networks. Use unicast mode or static device addressing.

#### UDP Protocols Not Responding
Ensure UDP port mappings are correctly configured in `docker-compose.yml`.

### Tool Installation Issues

If tools are missing:
```bash
# Rebuild Kali container
docker-compose build --no-cache kali

# Manually install tools
docker exec -it opel-kali /bin/bash
# Then install tools manually
```

## Best Practices

1. **Always use isolated networks** - Never connect OPEL to production systems
2. **Document findings** - Use the provided templates for consistent reporting
3. **Follow IEC 62443** - Align assessments with IEC 62443 standards
4. **Safety first** - Ensure all testing is authorized and safe
5. **Regular updates** - Keep tools and dependencies updated

## Advanced Usage

### Custom Protocol Simulators

Add custom protocol simulators in `ot-simulator/config/protocols/` and update `start-simulators.sh`.

### Custom Scan Scripts

Add custom scan scripts in `kali/tools/` and make them executable.

### Integration with External Tools

OPEL can be integrated with external tools via:
- Volume mounts for data exchange
- Network connectivity (if needed)
- API endpoints (if implemented)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the documentation
3. Open an issue on the repository

---

**Remember**: Always ensure you have proper authorization before conducting security assessments!


