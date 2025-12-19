# OPEL Quick Start Guide

This guide will help you get started with OPEL (OT Pentest Lab) quickly.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Network access (for initial setup and downloading dependencies)

## Starting the Lab

### 1. Build and Start Containers

From the OPEL directory, run:

```bash
docker compose up --build
```

This will:
- Build both containers (Kali and OT Simulator) if not already built
- Start all services (Kali and OT Simulator)
- Display logs from all containers

**Note**: The first time you run this, it may take several minutes to build the containers.

### 2. Run in Background (Detached Mode)

To run the lab in the background:

```bash
docker compose up -d
```

This starts the containers in detached mode, allowing you to continue using your terminal.

### 3. View Logs

If running in detached mode, view logs with:

```bash
# View all logs
docker compose logs -f

# View only Kali logs
docker compose logs -f kali

# View only OT simulator logs
docker compose logs -f ot-simulator
```

## Accessing the Kali Container

### Method 1: Using docker exec (Recommended)

While the containers are running, open a new terminal and run:

```bash
docker exec -it opel-kali /bin/bash
```

This gives you an interactive bash shell inside the Kali container.

### Method 2: Using docker compose exec

Alternatively, you can use:

```bash
docker compose exec kali /bin/bash
```

### Method 3: Access from Running Container

If you started the container with `docker compose up` (not detached), you can also access it from another terminal using either method above.

## First Steps in Kali Container

Once inside the Kali container, you'll be in `/root`. Here's what you can do:

### 1. Check Network Connectivity

Verify you can reach the OT simulator:

```bash
ping -c 3 ot-simulator
```

### 2. Check Available Tools

```bash
# List custom tools
ls -la /root/tools/

# Check if tools are executable
ls -la /root/tools/*.sh
```

### 3. Run OT Network Scan

```bash
cd /root/tools
./scan-ot.sh
```

This will scan the OT simulator for all protocols and save results to `/root/reports/scans/`.

### 4. Gather Intelligence

```bash
cd /root/tools
./intel-gather.sh
```

This collects OSINT data, threat intelligence, and vulnerability information.

### 5. Collect Data for Reporting

```bash
cd /root/tools
./collect-data.sh
```

This organizes all scan results and intelligence data for report generation.

## Accessing the OT Simulator Container

To access the OT simulator container:

```bash
docker exec -it opel-ot-simulator /bin/bash
```

Or using docker compose:

```bash
docker compose exec ot-simulator /bin/bash
```

## Running Conpot Manually

Conpot is an ICS honeypot that is installed in the OT simulator container but not started automatically. You can run it manually when needed.

### Prerequisites

- The OT simulator container must be running
- Access to the container (see "Accessing the OT Simulator Container" above)

### Steps to Run Conpot

1. **Access the OT simulator container:**
   ```bash
   docker exec -it opel-ot-simulator /bin/bash
   ```

2. **Switch to the conpot user:**
   ```bash
   su - conpot
   ```
   
   **Note**: Conpot refuses to run as root for security reasons, so you must switch to the `conpot` user.

3. **Activate the virtual environment:**
   ```bash
   source /opt/conpot/.venv/bin/activate
   ```

4. **Run Conpot:**
   ```bash
   conpot -f -t default
   ```
   
   **Flags explained:**
   - `-f` or `--foreground`: Run in foreground mode (see output in terminal)
   - `-t default` or `--template default`: Use the default template

### Running Conpot in Background

To run Conpot in the background (detached mode):

```bash
# From the conpot user shell
conpot -t default &
```

Or use `nohup` to keep it running after you exit:

```bash
nohup conpot -t default > /app/logs/conpot.log 2>&1 &
```

### Using Custom Configuration

If you have a custom Conpot configuration file:

```bash
conpot -f --config /path/to/custom/conpot.xml
```

### Checking Conpot Status

To check if Conpot is running:

```bash
# From root user in container
ps aux | grep conpot

# Check listening ports
netstat -tuln | grep -E "(5020|10201|16100|47808|6230|44818|2121|6969|8800)"
```

### Troubleshooting

- **"Can't start conpot with root"**: Make sure you've switched to the `conpot` user with `su - conpot`
- **"No module named conpot"**: Activate the virtual environment with `source /opt/conpot/.venv/bin/activate`
- **Permission denied**: Ensure `/opt/conpot` and `/app/logs` are owned by the `conpot` user

### Check Running Simulators

Inside the OT simulator container:

```bash
# Check running processes
ps aux | grep -E "(modbus|dnp3|bacnet|ethernetip|s7|iec104)"

# Check listening ports
netstat -tuln | grep -E "(502|102|2404|20000|47808|2222)"
```

## Stopping the Lab

### Stop Containers (Keep Data)

```bash
docker compose stop
```

### Stop and Remove Containers (Keep Data)

```bash
docker compose down
```

### Stop and Remove Everything (Including Volumes)

```bash
docker compose down -v
```

**Warning**: This will remove all data including scan results and intelligence data.

## Common Commands

### Restart Containers

```bash
docker compose restart
```

### Rebuild Containers

```bash
docker compose build --no-cache
```

### View Container Status

```bash
docker compose ps
```

### View Container Logs

```bash
# All containers
docker compose logs

# Specific container
docker compose logs kali
docker compose logs ot-simulator

# Follow logs (real-time)
docker compose logs -f
```

## File Locations

### Inside Kali Container

- **Tools**: `/root/tools/`
- **Reports**: `/root/reports/`
- **Intelligence Data**: `/root/intel/`
- **Report Templates**: `/root/reports/` (engagement-template.md, risk-assessment-template.md, remediation-template.md)

### On Host Machine

- **Reports**: `./kali/reports/` (mounted from container)
- **Intelligence**: `./intel/` (mounted from container)
- **OT Simulator Logs**: `./ot-simulator/logs/` (mounted from container)
- **OT Simulator Config**: `./ot-simulator/config/` (mounted from container)

## Troubleshooting

### Cannot Access Kali Container

If `docker exec` fails:

1. Check if container is running:
   ```bash
   docker compose ps
   ```

2. Check container logs:
   ```bash
   docker compose logs kali
   ```

3. Restart the container:
   ```bash
   docker compose restart kali
   ```

### OT Simulator Not Responding

1. Check if simulators are running:
   ```bash
   docker exec opel-ot-simulator ps aux | grep -E "(modbus|dnp3|bacnet|ethernetip|s7|iec104)"
   ```

2. Check simulator logs:
   ```bash
   docker compose logs ot-simulator
   ```

3. Restart the simulator:
   ```bash
   docker compose restart ot-simulator
   ```

### Network Connectivity Issues

1. Test connectivity from Kali:
   ```bash
   docker exec opel-kali ping -c 3 ot-simulator
   ```

2. Check network configuration:
   ```bash
   docker network inspect opel_opel-lab
   ```

3. Verify port mappings:
   ```bash
   docker port opel-ot-simulator
   ```

## Next Steps

1. **Run Scans**: Use `./scan-ot.sh` to scan the OT simulator
2. **Gather Intelligence**: Use `./intel-gather.sh` for OSINT and threat intelligence
3. **Generate Reports**: Use the templates in `/root/reports/` to create assessment reports
4. **Read Documentation**: Check `docs/usage.md` for detailed usage instructions
5. **Learn Protocols**: Review `docs/protocols.md` for protocol-specific information

## Example Workflow

```bash
# 1. Start the lab
docker compose up -d

# 2. Access Kali container
docker exec -it opel-kali /bin/bash

# 3. Inside Kali, run scans
cd /root/tools
./scan-ot.sh

# 4. Gather intelligence
./intel-gather.sh

# 5. Collect data for reports
./collect-data.sh

# 6. View results
ls -la /root/reports/scans/
ls -la /root/reports/collected_data/

# 7. Exit container
exit

# 8. Stop the lab when done
docker compose down
```

## Getting Help

- **Usage Guide**: See `docs/usage.md` for detailed instructions
- **Protocol Documentation**: See `docs/protocols.md` for protocol details
- **IEC 62443 Guide**: See `docs/IEC62443-guide.md` for compliance information
- **Main README**: See `README.md` for overview and architecture

---

**Remember**: Always ensure you have proper authorization before conducting security assessments!

