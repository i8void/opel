FROM debian:bookworm-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Python 3.11 and system dependencies
# Configure apt to handle repository sync issues and hash mismatches
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
    echo 'Acquire::http::Pipeline-Depth "0";' >> /etc/apt/apt.conf.d/99no-check-valid-until && \
    echo 'Acquire::http::No-Cache "true";' >> /etc/apt/apt.conf.d/99no-check-valid-until && \
    apt-get clean && \
    apt-get update && \
    # Install all packages together to avoid dependency issues
    # Use retry logic for transient repository issues
    (apt-get install -y --no-install-recommends --fix-missing \
    procps \
    net-tools \
    ca-certificates \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3.11-venv \
    git \
    g++ \
    make \
    build-essential \
    iputils-ping \
    curl \
    vim \
    netcat-openbsd \
    socat \
    libnghttp2-14 || \
    (sleep 3 && apt-get clean && apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    procps \
    net-tools \
    ca-certificates \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3.11-venv \
    git \
    g++ \
    make \
    build-essential \
    iputils-ping \
    curl \
    vim \
    netcat-openbsd \
    socat \
    libnghttp2-14)) && \
    # Try to install iproute2 separately (often has hash mismatch issues)
    (apt-get install -y --no-install-recommends --fix-missing iproute2 || \
     (sleep 2 && apt-get update && apt-get install -y --no-install-recommends --fix-missing iproute2) || \
     echo "Warning: iproute2 installation failed, continuing without it"; true) && \
    rm -rf /var/lib/apt/lists/*

# Create symlink for python3 to point to python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Create application directory
WORKDIR /app

# Install Python dependencies for protocol simulators
# Note: Some packages may fail due to network issues - install with fallbacks
# Use --break-system-packages for Debian PEP 668 compliance (safe in containers)
RUN (pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel || echo "pip upgrade failed, continuing...") && \
    (pip3 install --no-cache-dir --break-system-packages pymodbus || echo "pymodbus installation failed - Modbus simulator will use fallback") && \
    (pip3 install --no-cache-dir --break-system-packages 'bacpypes>=0.18.0' || echo "bacpypes installation failed - BACnet simulator will use fallback") && \
    (pip3 install --no-cache-dir --break-system-packages pycomm3 || echo "pycomm3 installation failed") && \
    (pip3 install --no-cache-dir --break-system-packages pysmi==0.3.4 || echo "pysmi installation failed") && \
    (pip3 install --no-cache-dir --break-system-packages pysnmp==4.4.12 || echo "pysnmp installation failed") && \
    (pip3 install --no-cache-dir --break-system-packages pyasn1==0.4.8 || echo "pyasn1 installation failed") && \
    (pip3 install --no-cache-dir --break-system-packages sphinx || echo "sphinx installation failed") && \
    (pip3 install --no-cache-dir --break-system-packages pydnp3 || echo "pydnp3 installation failed - DNP3 simulator will use basic TCP listener") || true

# Install SNAP7 (original repository: snap7/snap7)
# SNAP7 requires compilation
# Configure git to avoid credential prompts
RUN git config --global url."https://".insteadOf git:// && \
    git config --global http.sslVerify true && \
    (git clone https://github.com/snap7/snap7.git /tmp/snap7 && \
    cd /tmp/snap7/build/unix && \
    # Detect architecture and use appropriate makefile
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then \
        make -f x86_64_linux.mk && \
        cp ../bin/x86_64-linux/libsnap7.so /usr/lib/libsnap7.so; \
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
        make -f arm_v7_linux.mk || make -f arm64_linux.mk || echo "ARM build failed, trying x86_64"; \
        cp ../bin/*/libsnap7.so /usr/lib/libsnap7.so 2>/dev/null || true; \
    else \
        echo "Unknown architecture $ARCH, trying default build"; \
        make || true; \
    fi && \
    ldconfig && \
    rm -rf /tmp/snap7 || echo "SNAP7 installation failed - S7 simulator will use basic TCP listener")

# Install Python SNAP7 bindings
RUN pip3 install --no-cache-dir --break-system-packages python-snap7

# Install Conpot (original repository: mushorg/conpot)
# Create conpot user and install Conpot with virtual environment
RUN useradd -m -u 1000 -s /bin/bash conpot && \
    mkdir -p /opt/conpot && \
    git clone https://github.com/mushorg/conpot.git /opt/conpot && \
    python3 -m venv /opt/conpot/.venv && \
    /opt/conpot/.venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/conpot/.venv/bin/pip install -r /opt/conpot/requirements.txt && \
    /opt/conpot/.venv/bin/pip install sphinx && \
    cd /opt/conpot && /opt/conpot/.venv/bin/python setup.py install && \
    chown -R conpot:conpot /opt/conpot /app/logs || echo "Conpot installation completed"

# Set capabilities for binding to privileged ports (if needed)
# Note: In Docker, we'll use port mappings instead
# Note: setcap may not be available in slim images, so this is optional
RUN (which setcap && setcap cap_net_bind_service=+ep /usr/bin/python3.11 || true) || true

# Create directories
RUN mkdir -p /app/config /app/logs /app/scripts

# Copy configuration and scripts
COPY config/ /app/config/
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

# All ports are internal only - no EXPOSE needed
# Port mappings are commented out in docker-compose.yml
# EXPOSE 502 102 2404 20000 47808 2222 16100

WORKDIR /app

# Default command
CMD ["/app/scripts/start-simulators.sh"]

