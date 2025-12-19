# OPEL - OT Pentest Lab

**OPEL** (OT Pentest Lab) is a Docker-based Operational Technology penetration testing laboratory designed for educational purposes and customer engagements. It follows IEC 62443 standards and emphasizes safety, intelligence gathering, risk assessment, and structured reporting.

## Overview

OPEL provides a complete environment for:
- Simulating various OT protocols (Modbus, S7, IEC 104, DNP3, BACnet, EtherNet/IP)
- Conducting security assessments and penetration testing
- Gathering intelligence from OSINT and threat intelligence sources
- Performing risk assessments aligned with IEC 62443
- Generating comprehensive reports for customer engagements

## Architecture

OPEL consists of two main containers:
- **Kali Linux Container**: Investigator toolbox with OT-specific scanning tools and intelligence gathering capabilities
- **OT Simulator Container**: Minimal Linux container running multiple protocol simulators (Modbus, S7, IEC 104, DNP3, BACnet, EtherNet/IP)

## Quick Start

**For detailed step-by-step instructions, see [QUICKSTART.md](QUICKSTART.md)**

### Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Network access for downloading dependencies (initial setup only)

### Quick Commands

1. Build and start the lab:
```bash
docker compose up --build
```

2. Access Kali container (in a new terminal):
```bash
docker exec -it opel-kali /bin/bash
```

3. Run your first scan:
```bash
cd /root/tools
./scan-ot.sh
```

See [QUICKSTART.md](QUICKSTART.md) for complete instructions, troubleshooting, and examples.

### First Steps

1. **Start the OT simulators** (in ot-simulator container):
   - Simulators start automatically when the container starts
   - Check logs: `docker logs opel-ot-simulator`

2. **Run scans** (in Kali container):
```bash
cd /root/tools
./scan-ot.sh
```

3. **Gather intelligence**:
```bash
./intel-gather.sh
```

4. **Collect data for reporting**:
```bash
./collect-data.sh
```

## Project Structure

```ascii
opel/
├── docker-compose.yml          # Main orchestration
├── README.md                   # This file
├── kali/                       # Kali Linux container
│   ├── Dockerfile
│   ├── tools/                 # Custom scanning and intelligence scripts
│   └── reports/               # Report templates
├── ot-simulator/              # OT simulator container
│   ├── Dockerfile
│   ├── config/                # Simulator configurations
│   │   └── protocols/
│   └── scripts/               # Startup scripts
├── intel/                     # Intelligence data storage
│   ├── osint/
│   ├── threat-intel/
│   └── vuln-db/
└── docs/                      # Documentation
    ├── usage.md
    ├── IEC62443-guide.md
    └── protocols.md
```

## Features

- **Comprehensive Protocol Support**: Modbus TCP, S7 (Siemens), IEC 104, DNP3, BACnet/IP, EtherNet/IP
- **OT-Specific Tools**: Nmap with ICS scripts, PLCscan, Modbus-cli, ICSSecurityScripts
- **Intelligence Gathering**: OSINT tools, threat intelligence feeds, vulnerability databases
- **IEC 62443 Compliance**: Risk assessment templates and reporting aligned with IEC 62443
- **Safety First**: Isolated Docker network, no production connectivity
- **Educational**: Comprehensive documentation and learning paths

## Protocols Supported

| Protocol | Port | Transport | Status |
|----------|------|-----------|--------|
| Modbus TCP | 502 | TCP |  Fully Supported |
| S7 (Siemens) | 102 | TCP |  Fully Supported |
| IEC 104 | 2404 | TCP |  Supported |
| DNP3 | 20000 | TCP |  Supported |
| BACnet/IP | 47808 | UDP |  Supported (unicast mode) |
| EtherNet/IP | 2222 | TCP/UDP |  Supported |

## Networking Considerations

Docker bridge networks support TCP and UDP unicast traffic. Some protocols (like BACnet/IP) use multicast for device discovery, which may not work reliably in Docker bridge networks. OPEL is configured to use unicast mode for these protocols, which is sufficient for penetration testing scenarios.

See [docs/protocols.md](docs/protocols.md) for detailed protocol documentation.

## Safety and Security

 **IMPORTANT**: This lab is designed for **educational purposes and authorized testing only**.

- The lab uses an isolated Docker network with no host network access
- Never connect this lab to production systems
- All testing should be conducted in isolated environments
- Follow responsible disclosure practices for any vulnerabilities found

## Documentation

- [Usage Guide](docs/usage.md) - Detailed usage instructions
- [IEC 62443 Guide](docs/IEC62443-guide.md) - IEC 62443 compliance guide
- [Protocol Documentation](docs/protocols.md) - Protocol-specific documentation

## Report Templates

Report templates are available in `kali/reports/`:
- `engagement-template.md` - Customer engagement report template
- `risk-assessment-template.md` - IEC 62443 risk assessment template
- `remediation-template.md` - Remediation tracking template

## Contributing

Contributions are welcome! Please ensure:
- All tools use original maintainer repositories (not forks)
- Safety and security best practices are followed
- Documentation is updated accordingly


## Disclaimer

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before conducting any security assessments. The authors and contributors are not responsible for any misuse of this tool.

## Support

For issues, questions, or contributions, please [open an issue]((https://github.com/i8void/opel/issues).

---

**OPEL** - Building safer OT environments through education and assessment.

