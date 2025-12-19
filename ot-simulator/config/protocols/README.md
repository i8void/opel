# Protocol Simulator Configuration

This directory contains configuration files and scripts for OT protocol simulators.

## Available Simulators

- **modbus_server.py** - Modbus TCP simulator (port 502)
- **s7_server.py** - S7/Siemens simulator (port 102)
- **iec104_server.py** - IEC 104 simulator (port 2404)
- **dnp3_server.py** - DNP3 simulator (port 20000)
- **bacnet_server.py** - BACnet/IP simulator (port 47808/UDP)
- **ethernetip_server.py** - EtherNet/IP simulator (port 2222)

## Configuration

Each simulator can be configured via environment variables in `docker-compose.yml`:

- `MODBUS_ENABLED=true/false`
- `S7_ENABLED=true/false`
- `IEC104_ENABLED=true/false`
- `DNP3_ENABLED=true/false`
- `BACNET_ENABLED=true/false`
- `ETHERNETIP_ENABLED=true/false`

## Customization

To customize a simulator:

1. Edit the corresponding Python script in this directory
2. Modify configuration parameters
3. Rebuild the container: `docker-compose build ot-simulator`
4. Restart: `docker-compose restart ot-simulator`

## Logs

Simulator logs are stored in `/app/logs/` inside the container and mounted to `ot-simulator/logs/` on the host.

## Troubleshooting

If a simulator fails to start:

1. Check logs: `docker logs opel-ot-simulator`
2. Verify port availability: `docker exec opel-ot-simulator netstat -tuln`
3. Check script permissions: `docker exec opel-ot-simulator ls -la /app/config/protocols/`


