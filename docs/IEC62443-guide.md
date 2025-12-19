# IEC 62443 Compliance Guide

This guide explains how OPEL aligns with IEC 62443 standards and how to conduct assessments in compliance with these standards.

## Table of Contents

1. [Introduction to IEC 62443](#introduction-to-iec-62443)
2. [IEC 62443 Structure](#iec-62443-structure)
3. [Security Levels](#security-levels)
4. [Security Zones and Conduits](#security-zones-and-conduits)
5. [Purdue Model and IEC 62443 Zones](#purdue-model-and-iec-62443-zones)
6. [Fundamental Requirements](#fundamental-requirements)
7. [Using OPEL for IEC 62443 Assessments](#using-opel-for-iec-62443-assessments)
8. [Reporting Compliance](#reporting-compliance)

## Introduction to IEC 62443

IEC 62443 is an international series of standards that provides a framework for addressing cybersecurity in industrial automation and control systems (IACS). The standards are designed to help organizations:

- Identify and assess security risks
- Implement appropriate security controls
- Maintain security throughout the system lifecycle
- Ensure safety and availability are not compromised

## IEC 62443 Structure

The IEC 62443 series is organized into multiple parts:

### Part 1: General
- **IEC 62443-1-1**: Terminology, concepts, and models
- **IEC 62443-1-2**: Master glossary of terms and abbreviations
- **IEC 62443-1-3**: System security conformance metrics
- **IEC 62443-1-4**: IACS security lifecycle and use cases

### Part 2: Policies and Procedures
- **IEC 62443-2-1**: Security program requirements
- **IEC 62443-2-2**: Security program implementation
- **IEC 62443-2-3**: Patch management
- **IEC 62443-2-4**: Security program requirements for IACS service providers

### Part 3: System Requirements
- **IEC 62443-3-1**: Security technologies
- **IEC 62443-3-2**: Security risk assessment
- **IEC 62443-3-3**: System security requirements and security levels

### Part 4: Component Requirements
- **IEC 62443-4-1**: Product development lifecycle
- **IEC 62443-4-2**: Technical security requirements

## Security Levels

IEC 62443 defines four Security Levels (SL) that represent increasing levels of security:

### SL1: Protection against Casual or Coincidental Violation
- Basic security measures
- Protection against unintentional access
- Suitable for non-critical systems

### SL2: Protection against Intentional Violation Using Simple Means
- Enhanced security measures
- Protection against attackers with limited resources
- Suitable for most industrial systems

### SL3: Protection against Intentional Violation Using Sophisticated Means
- Advanced security measures
- Protection against skilled attackers
- Suitable for critical systems

### SL4: Protection against Intentional Violation Using Sophisticated Means with Extended Resources
- Highest level of security
- Protection against nation-state level threats
- Suitable for highly critical systems

## Security Zones and Conduits

### Security Zones

A **Security Zone** is a grouping of logical or physical assets that share common security requirements based on:
- Criticality
- Functionality
- Security level requirements

Zones should be:
- Clearly defined
- Logically or physically separated
- Protected by appropriate security controls

### Conduits

A **Conduit** is a communication path between security zones. Conduits must:
- Control data flow between zones
- Enforce security policies
- Monitor and log communications
- Prevent unauthorized access

### Zone and Conduit Design Principles

1. **Least Privilege**: Grant minimum necessary access
2. **Defense in Depth**: Multiple layers of security
3. **Segmentation**: Isolate critical systems
4. **Monitoring**: Continuous monitoring of zone boundaries

## Purdue Model and IEC 62443 Zones

The Purdue Model (ISA-95) provides a hierarchical framework for industrial control systems, while IEC 62443 defines security zones based on security requirements. Understanding the relationship between these models is essential for proper security architecture.

### Purdue Levels and IEC 62443 Zone Mapping

| Purdue Level | IEC 62443 Zone (typical) | Typical Devices | Common Protocols | Usually Communicates With |
|---|---|---|---|---|
| **Level 0** | Field Zone | Sensors, actuators, drives, valves | 4–20 mA, HART, CAN, IO-Link | PLCs (L1) |
| **Level 1** | Control Zone | PLCs, RTUs, safety controllers | Modbus RTU/TCP, PROFINET, EtherNet/IP, S7 (102), DNP3, IEC 61850 | Field devices (L0), HMIs/SCADA (L2) |
| **Level 2** | Supervisory Zone | HMIs, local SCADA, engineering stations | OPC Classic, OPC UA, Modbus TCP, BACnet, SNMP | PLCs (L1), Operations systems (L3) |
| **Level 3** | Operations Zone | Historians, batch systems, OT servers | OPC UA, SQL, MQTT, HTTPS, Syslog | SCADA/HMI (L2), DMZ services (L3.5) |
| **Level 3.5** | Industrial DMZ | Proxies, jump hosts, data brokers | HTTPS, MQTT, OPC UA (terminated), SFTP | L3 systems ↔ Enterprise (L4) |
| **Level 4** | Enterprise Zone | ERP, MES, AD, reporting | HTTPS, SQL, LDAP, REST APIs | DMZ (L3.5), IT systems |
| **Level 5** | External Zone | Cloud, vendors, partners | HTTPS, VPN, MQTT, APIs | Enterprise / DMZ only |

### Key Takeaways

- **ICS protocols cluster at Levels 0–2** because they control physical processes.
- **Higher levels use IT protocols** and only see *aggregated or terminated* OT data.
- **IEC 62443 enforces separation via zones and conduits**, not by inventing new control protocols.

### Communication Matrix: What Must Never Talk Directly

The following matrix shows which levels should **never** communicate directly with each other, requiring proper conduits and security controls:

| From Level | To Level | Direct Communication | Required Conduit |
|---|---|---|---|
| **Level 0** | Level 2+ |**NEVER** | Must go through Level 1 (PLC) |
| **Level 0** | Level 3+ |  **NEVER** | Must go through Level 0 → Level 2 → Level 3 |
| **Level 1** | Level 3+ |  **NEVER** | Must go through Level 2 (SCADA/HMI) |
| **Level 1** | Level 4+ |  **NEVER** | Must go through Level 2 → Level 3 → DMZ |
| **Level 2** | Level 4+ |  **NEVER** | Must go through Level 3 → DMZ |
| **Level 2** | Level 5 |  **NEVER** | Must go through Level 3 → DMZ → Enterprise |
| **Level 3** | Level 5 |  **NEVER** | Must go through DMZ → Enterprise |
| **Level 4** | Level 0-2 |  **NEVER** | Must go through DMZ → Level 3 → Level 2 |
| **Level 5** | Level 0-3 |  **NEVER** | Must go through Enterprise → DMZ → Level 3 |

**Critical Rules:**
- **Level 0 devices should ONLY communicate with Level 1** (PLCs/RTUs)
- **Level 1 devices should ONLY communicate with Level 0 and Level 2**
- **Level 2 systems should ONLY communicate with Level 1 and Level 3**
- **Level 3 systems should ONLY communicate with Level 2 and DMZ (L3.5)**
- **Level 4/5 should NEVER directly access Level 0-2**


\newpage
### Secure Reference Flow

The following diagram illustrates the proper secure communication flow in an industrial control system:

```ascii
┌─────────────────────────────────────────────────────────────────┐
│                        Level 5: External Zone                   │
│                    (Cloud, Vendors, Partners)                   │
│                    Protocols: HTTPS, VPN, APIs                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTPS/VPN (Authenticated)
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    Level 4: Enterprise Zone                     │
│              (ERP, MES, Active Directory, Reporting)            │
│              Protocols: HTTPS, SQL, LDAP, REST APIs             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTPS, SQL (Authenticated)
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                   Level 3.5: Industrial DMZ                     │
│         (Proxies, Jump Hosts, Data Brokers, Firewalls)          │
│     Protocols: HTTPS, MQTT, OPC UA (terminated), SFTP           │
│                    [SECURITY BOUNDARY]                          │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ OPC UA, MQTT, HTTPS (Terminated)
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    Level 3: Operations Zone                     │
│         (Historians, Batch Systems, OT Servers, MES)            │
│              Protocols: OPC UA, SQL, MQTT, HTTPS                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ OPC Classic/UA, Modbus TCP
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                   Level 2: Supervisory Zone                     │
│        (HMIs, Local SCADA, Engineering Stations)                │
│      Protocols: OPC Classic, OPC UA, Modbus TCP, BACnet         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Modbus, PROFINET, EtherNet/IP
                               │ S7 (102), DNP3, IEC 61850
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     Level 1: Control Zone                       │
│              (PLCs, RTUs, Safety Controllers)                   │
│    Protocols: Modbus RTU/TCP, PROFINET, EtherNet/IP, S7         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ 4-20 mA, HART, CAN, IO-Link
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      Level 0: Field Zone                        │
│            (Sensors, Actuators, Drives, Valves)                 │
│              Protocols: 4-20 mA, HART, CAN, IO-Link             │
└─────────────────────────────────────────────────────────────────┘
```

### Secure Communication Principles

1. **Unidirectional Data Flow (Down)**: Commands and setpoints flow from higher levels to lower levels
2. **Unidirectional Data Flow (Up)**: Process data and status flow from lower levels to higher levels
3. **No Direct Cross-Level Communication**: Levels must communicate through adjacent levels only
4. **DMZ as Security Boundary**: Level 3.5 (DMZ) acts as the critical security boundary between OT and IT
5. **Protocol Termination**: OT protocols (Modbus, OPC Classic) should be terminated at the DMZ and converted to IT protocols (HTTPS, MQTT)
6. **Authentication Required**: All cross-zone communication must be authenticated
7. **Monitoring and Logging**: All conduits must be monitored and logged

### Implementation in OPEL

When using OPEL for assessments:

1. **Map Network Topology**: Identify which devices are at which Purdue levels
2. **Identify Zone Boundaries**: Map Purdue levels to IEC 62443 zones
3. **Verify Communication Paths**: Ensure no direct communication between non-adjacent levels
4. **Check Conduit Security**: Verify that conduits have proper security controls
5. **Document Violations**: Identify any direct communication that violates the secure reference flow
6. **Recommend Remediation**: Suggest proper conduits and security controls for violations

## Fundamental Requirements

IEC 62443-3-3 defines seven Fundamental Requirements (FR):

### FR-1: Identification and Authentication Control
- User identification and authentication
- Device authentication
- Strong password policies
- Multi-factor authentication (for SL3/SL4)

### FR-2: Use Control
- Access control based on roles
- Principle of least privilege
- Session management
- Audit logging

### FR-3: System Integrity
- Protection against unauthorized changes
- Code signing and verification
- Secure update mechanisms
- Integrity monitoring

### FR-4: Data Confidentiality
- Encryption of sensitive data
- Secure communication protocols
- Key management
- Data classification

### FR-5: Restricted Data Flow
- Network segmentation
- Firewall rules
- Data flow policies
- Zone boundary protection

### FR-6: Timely Response to Events
- Security event detection
- Incident response procedures
- Logging and monitoring
- Alert mechanisms

### FR-7: Resource Availability
- Denial of service protection
- Redundancy and failover
- Performance monitoring
- Capacity planning

## Using OPEL for IEC 62443 Assessments

### 1. Zone Identification

Use OPEL to:
- Map network topology
- Identify communication paths
- Document zone boundaries
- Identify conduits

Tools:
- Network scanning (`scan-ot.sh`)
- Protocol analysis
- Network mapping

### 2. Security Level Assessment

Assess current security levels:
- Review security controls
- Test access controls
- Evaluate monitoring capabilities
- Assess incident response

### 3. Vulnerability Assessment

Identify vulnerabilities:
- Protocol-specific vulnerabilities
- Network security issues
- Access control weaknesses
- System integrity issues

### 4. Risk Assessment

Evaluate risks:
- Likelihood of exploitation
- Impact on operations
- Safety implications
- Availability concerns

### 5. Compliance Verification

Verify compliance with:
- Fundamental Requirements (FR)
- Security Level requirements
- Zone and conduit requirements
- Organizational policies

## Reporting Compliance

### Risk Assessment Report

Use the `risk-assessment-template.md` to document:
- Zone and conduit identification
- Security level assessment
- Vulnerability findings
- Risk matrix
- Compliance status
- Remediation recommendations

### Key Sections for IEC 62443 Compliance

1. **Executive Summary**
   - Overall compliance status
   - Key findings
   - Risk posture

2. **Security Zones and Conduits**
   - Zone identification
   - Conduit documentation
   - Security controls

3. **Security Level Assessment**
   - Current SL vs. Target SL
   - Gap analysis
   - Component-level SL assessment

4. **Fundamental Requirements Assessment**
   - FR-1 through FR-7 status
   - Evidence of compliance
   - Non-compliance issues

5. **Risk Assessment**
   - Risk matrix
   - Risk categorization
   - Safety and availability considerations

6. **Remediation Recommendations**
   - Prioritized actions
   - Security level improvements
   - Compliance roadmap

## Best Practices

1. **Safety First**: Never compromise safety or availability
2. **Documentation**: Maintain detailed documentation
3. **Continuous Assessment**: Regular security assessments
4. **Stakeholder Engagement**: Involve all relevant stakeholders
5. **Remediation Tracking**: Track and verify remediation actions

## Resources

- IEC 62443 Official Documentation
- ICS-CERT Advisories
- NIST Cybersecurity Framework
- Industry-specific guidelines

## Conclusion

OPEL provides tools and templates to conduct IEC 62443-compliant assessments. By following this guide and using the provided templates, you can:

- Conduct thorough security assessments
- Document findings in compliance with IEC 62443
- Provide actionable remediation recommendations
- Support customer engagements with standardized reporting

---

**Remember**: IEC 62443 compliance is an ongoing process, not a one-time activity. Regular assessments and continuous improvement are essential.


