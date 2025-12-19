# OT Protocol Documentation

This document provides detailed information about the OT protocols supported in OPEL, including their characteristics, security considerations, and testing approaches.

## Table of Contents

1. [Modbus TCP](#modbus-tcp)
2. [S7 (Siemens)](#s7-siemens)
3. [IEC 104](#iec-104)
4. [DNP3](#dnp3)
5. [BACnet/IP](#bacnetip)
6. [EtherNet/IP](#ethernetip)
7. [Protocol Security Considerations](#protocol-security-considerations)

## Modbus TCP

### Overview
Modbus TCP is a widely used industrial communication protocol that operates over TCP/IP. It's commonly used in SCADA systems and PLCs.

### Characteristics
- **Port**: 502 (TCP)
- **Transport**: TCP
- **Function Codes**: Read/Write operations (0x01-0x17)
- **Data Types**: Coils, Discrete Inputs, Holding Registers, Input Registers

### Security Considerations
- **No Authentication**: Modbus TCP has no built-in authentication
- **No Encryption**: Data is transmitted in plaintext
- **Vulnerable to**: Man-in-the-middle attacks, unauthorized access, data manipulation

### Testing with OPEL
```bash
# Nmap scan
nmap -p 502 --script modbus-discover,modbus-read-registers ot-simulator

# Modbus-cli
modbus read ot-simulator 502 1 0 10
```

### Common Vulnerabilities
- Unauthorized read/write access
- Lack of authentication
- Plaintext data transmission
- No integrity checking

## S7 (Siemens)

### Overview
S7 is Siemens' proprietary communication protocol used for communication with S7 PLCs. It operates over TCP/IP.

### Characteristics
- **Port**: 102 (TCP)
- **Transport**: TCP
- **Protocol**: ISO-on-TCP (RFC 1006)
- **Functions**: Read/Write memory, control operations

### Security Considerations
- **Limited Authentication**: Basic password protection (weak)
- **No Encryption**: Data transmitted in plaintext
- **Vulnerable to**: Unauthorized access, command injection, denial of service

### Testing with OPEL
```bash
# Nmap scan
nmap -p 102 --script s7-info ot-simulator

# Python SNAP7
python3 -c "import snap7; client = snap7.client.Client(); client.connect('ot-simulator', 0, 1)"
```

### Common Vulnerabilities
- Weak password protection
- Unauthorized command execution
- Plaintext communication
- Information disclosure

## IEC 104

### Overview
IEC 104 (IEC 60870-5-104) is a protocol for telecontrol, teleprotection, and associated telecommunications. It's commonly used in power systems.

### Characteristics
- **Port**: 2404 (TCP, default)
- **Transport**: TCP
- **Structure**: Application Service Data Unit (ASDU)
- **Functions**: Control commands, data acquisition, time synchronization

### Security Considerations
- **No Authentication**: No built-in authentication mechanism
- **No Encryption**: Data transmitted in plaintext
- **Vulnerable to**: Unauthorized control commands, data manipulation, replay attacks

### Testing with OPEL
```bash
# Nmap scan
nmap -p 2404 -sV ot-simulator

# Protocol analysis
# Requires specialized IEC 104 libraries
```

### Common Vulnerabilities
- Unauthorized control commands
- Lack of authentication
- Plaintext transmission
- Replay attacks

## DNP3

### Overview
DNP3 (Distributed Network Protocol) is used in SCADA systems, particularly in the electric utility industry.

### Characteristics
- **Port**: 20000 (TCP/UDP)
- **Transport**: TCP or UDP
- **Structure**: Application, Data Link, and Transport layers
- **Functions**: Data acquisition, control operations, event reporting

### Security Considerations
- **DNP3 Secure Authentication**: Optional authentication extension (DNP3-SA)
- **Encryption**: Available in secure variant
- **Vulnerable to**: Unauthorized access (if not using SA), replay attacks, denial of service

### Testing with OPEL
```bash
# Nmap scan
nmap -p 20000 --script dnp3-info ot-simulator
```

### Common Vulnerabilities
- Unauthorized access (if DNP3-SA not used)
- Replay attacks
- Denial of service
- Information disclosure

## BACnet/IP

### Overview
BACnet (Building Automation and Control Networks) is used in building automation systems. BACnet/IP is the IP-based variant.

### Characteristics
- **Port**: 47808 (UDP)
- **Transport**: UDP (with multicast support)
- **Functions**: Device discovery, object access, event/alarm management
- **Objects**: Analog Input/Output, Binary Input/Output, etc.

### Security Considerations
- **BACnet Secure Connect**: Optional security extension
- **Multicast**: Uses multicast for device discovery
- **Vulnerable to**: Unauthorized access, device spoofing, denial of service

### Testing with OPEL
```bash
# Nmap scan (UDP)
nmap -sU -p 47808 --script bacnet-info ot-simulator

# Note: Multicast discovery may not work in Docker bridge networks
# Use unicast mode or static device addressing
```

### Docker Networking Note
BACnet/IP uses multicast for device discovery, which may not work reliably in Docker bridge networks. OPEL is configured to use unicast mode, which is sufficient for penetration testing scenarios.

### Common Vulnerabilities
- Unauthorized device access
- Device spoofing
- Lack of authentication (if BACnet Secure Connect not used)
- Multicast-based attacks

## EtherNet/IP

### Overview
EtherNet/IP is an industrial Ethernet protocol used in automation systems. It's based on the Common Industrial Protocol (CIP).

### Characteristics
- **Port**: 2222 (TCP/UDP)
- **Transport**: TCP (explicit messaging) and UDP (implicit messaging)
- **Protocol**: CIP over TCP/UDP
- **Functions**: Device configuration, data exchange, control operations

### Security Considerations
- **CIP Security**: Optional security extension
- **No Default Encryption**: Standard EtherNet/IP has no encryption
- **Vulnerable to**: Unauthorized access, command injection, denial of service

### Testing with OPEL
```bash
# Nmap scan
nmap -p 2222 -sV ot-simulator
nmap -sU -p 2222 ot-simulator
```

### Common Vulnerabilities
- Unauthorized access
- Command injection
- Lack of authentication (if CIP Security not used)
- Denial of service

## Protocol Security Considerations

### Common Security Issues Across Protocols

1. **Lack of Authentication**
   - Most OT protocols lack strong authentication
   - Default or weak credentials are common
   - Recommendation: Implement network segmentation and access controls

2. **Plaintext Communication**
   - Most protocols transmit data in plaintext
   - Recommendation: Use VPNs or protocol-specific security extensions

3. **No Integrity Checking**
   - Data can be modified in transit
   - Recommendation: Implement network monitoring and anomaly detection

4. **Denial of Service**
   - Many protocols are vulnerable to DoS attacks
   - Recommendation: Implement rate limiting and network segmentation

5. **Information Disclosure**
   - Protocols often reveal system information
   - Recommendation: Limit network exposure and implement filtering

### Testing Methodology

1. **Discovery**
   - Network scanning
   - Protocol identification
   - Device enumeration

2. **Enumeration**
   - Protocol-specific enumeration
   - Data point discovery
   - Function identification

3. **Vulnerability Assessment**
   - Authentication testing
   - Authorization testing
   - Protocol-specific vulnerabilities

4. **Exploitation** (Authorized Only)
   - Proof of concept
   - Impact assessment
   - Remediation validation

### Best Practices

1. **Network Segmentation**
   - Isolate OT networks from IT networks
   - Implement zone boundaries
   - Use firewalls and access controls

2. **Monitoring**
   - Monitor network traffic
   - Detect anomalies
   - Log all access attempts

3. **Access Control**
   - Implement strong authentication
   - Use principle of least privilege
   - Regular access reviews

4. **Encryption**
   - Use VPNs for remote access
   - Implement protocol-specific security extensions where available
   - Encrypt sensitive communications

5. **Regular Assessments**
   - Conduct regular security assessments
   - Keep systems updated
   - Review and update security controls

## References

- Modbus: https://modbus.org/
- S7/SNAP7: https://sourceforge.net/projects/snap7/
- IEC 104: IEC 60870-5-104 standard
- DNP3: https://www.dnp.org/
- BACnet: https://www.bacnet.org/
- EtherNet/IP: https://www.odva.org/

---

**Note**: This documentation is for educational and authorized testing purposes only. Always ensure you have proper authorization before testing OT systems.


