# OT Simulator Configuration

This directory contains configuration files for the OT simulator container.

## Directory Structure

```
config/
├── protocols/           # Protocol simulator scripts
│   ├── modbus_server.py
│   ├── s7_server.py
│   ├── iec104_server.py
│   ├── dnp3_server.py
│   ├── bacnet_server.py
│   └── ethernetip_server.py
└── README.md            # This file
```

## Protocol Simulators

Individual protocol simulators are Python scripts in the `protocols/` directory. They can be enabled/disabled via environment variables in `docker-compose.yml`.

## Port Configuration

Default ports (can be changed in docker-compose.yml):
- Modbus TCP: 502
- S7: 102
- IEC 104: 2404
- DNP3: 20000
- BACnet/IP: 47808 (UDP)
- EtherNet/IP: 2222 (TCP/UDP)

## Network Considerations

- **TCP protocols**: Work perfectly in Docker
- **UDP protocols**: Work in Docker, but multicast may be limited
- **BACnet/IP**: Configured for unicast mode (Docker-friendly)

## Customization

To customize simulators:

1. Edit the Python scripts in `protocols/`
2. Rebuild container: `docker-compose build ot-simulator`
3. Restart: `docker-compose restart ot-simulator`

## Logs

All simulator logs are written to `/app/logs/` inside the container, which is mounted to `ot-simulator/logs/` on the host.


