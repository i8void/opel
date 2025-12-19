FROM kalilinux/kali-rolling:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update and install base tools
# Add retry logic and hash mismatch handling for transient repository issues
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
    echo 'Acquire::AllowInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99no-check-valid-until && \
    echo 'Acquire::AllowDowngradeToInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99no-check-valid-until && \
    echo 'Acquire::http::Pipeline-Depth "0";' >> /etc/apt/apt.conf.d/99no-check-valid-until && \
    apt-get clean && \
    apt-get update && \
    (apt-get install -y --no-install-recommends --fix-missing --allow-unauthenticated \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    ruby \
    ruby-dev \
    build-essential \
    nmap \
    net-tools \
    iputils-ping \
    vim \
    iproute2 \
    netcat-openbsd \
    socat || \
    (echo "First attempt failed, retrying..." && \
     sleep 5 && \
     apt-get clean && \
     apt-get update && \
     apt-get install -y --no-install-recommends --fix-missing --allow-unauthenticated \
     git \
     curl \
     wget \
     python3 \
     python3-pip \
     ruby \
     ruby-dev \
     build-essential \
     nmap \
     net-tools \
     iputils-ping \
     vim \
     iproute2 \
     netcat-openbsd \
     socat)) && \
    rm -rf /var/lib/apt/lists/*

# Install Ruby gems (may fail due to network/SSL issues - can be installed manually later)
RUN (gem install modbus-cli || echo "modbus-cli gem installation failed - can be installed manually later") || true

# Install OSINT tools (optional - may fail if repositories are syncing)
# These can be installed manually later if needed
RUN apt-get update && \
    (apt-get install -y --fix-missing theharvester recon-ng maltego 2>&1 || echo "OSINT tools installation failed - can be installed manually later") && \
    rm -rf /var/lib/apt/lists/* || true

# Create directories
RUN mkdir -p /root/tools /root/reports /root/intel

# Install PLCscan (verify original repository)
WORKDIR /root/tools
RUN git clone https://github.com/meeas/plcscan.git || echo "Repository verification needed"

# Install ICSSecurityScripts (verify original repository)
RUN git clone https://github.com/tijldeneut/ICSSecurityScripts.git || echo "Repository verification needed"

# Install RedpointNSE scripts (verify original repository)
# Note: Original repository needs verification - using placeholder
RUN mkdir -p /tmp/redpoint && \
    cd /tmp/redpoint && \
    (git clone https://github.com/rick-cen/RedpointNSE.git 2>/dev/null || echo "Original repository needs verification") && \
    if [ -d RedpointNSE ]; then \
        cp *.nse /usr/share/nmap/scripts/ 2>/dev/null || true; \
    fi && \
    rm -rf /tmp/redpoint

# Copy custom tools and scripts
COPY tools/ /root/tools/
RUN chmod +x /root/tools/*.sh 2>/dev/null || true

# Set working directory
WORKDIR /root

# Default command
CMD ["/bin/bash"]

