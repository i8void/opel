#!/usr/bin/env python3
"""
OPEL - DNP3 Simulator
Simple DNP3 server for testing and education
Note: Full DNP3 implementation requires specialized libraries
"""

import socket
import logging
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import pydnp3, fallback to simple TCP if not available
try:
    import pydnp3
    PYDNP3_AVAILABLE = True
except ImportError:
    PYDNP3_AVAILABLE = False

def run_dnp3_server_simple():
    """Simple DNP3 TCP listener (fallback)"""
    host = "0.0.0.0"
    port = 20000
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        
        logger.info(f"DNP3 simulator listening on {host}:{port}")
        logger.info("Note: This is a basic TCP listener. Full DNP3 protocol requires pydnp3 library.")
        
        while True:
            conn, addr = sock.accept()
            logger.info(f"DNP3 connection from {addr}")
            
            try:
                # DNP3 Application Layer Header (simplified)
                # Real DNP3 requires proper Link Layer and Transport Layer framing
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    logger.info(f"Received {len(data)} bytes: {data.hex()}")
                    
                    # Basic DNP3 response frame (simplified)
                    # DNP3 Link Layer: Start bytes (0x0564), Length, Control, Destination, Source
                    # This is a minimal response - real DNP3 requires proper protocol implementation
                    if len(data) >= 5:
                        # Echo back with DNP3-like structure
                        # Start bytes: 0x05 0x64
                        response = b'\x05\x64'
                        # Length (simplified)
                        response += struct.pack('B', min(len(data) + 5, 255))
                        # Control byte (Primary, User data, FIN=1, FIR=1)
                        response += b'\xC4'
                        # Destination and Source addresses (simplified)
                        response += data[3:5] if len(data) >= 5 else b'\x00\x00'
                        # Data (simplified echo)
                        response += data[5:] if len(data) > 5 else b''
                        
                        conn.send(response)
                        logger.info(f"Sent response: {response.hex()}")
                    else:
                        # Very short message, send basic acknowledgment
                        conn.send(b'\x05\x64\x05\xC4\x00\x00')
                        
            except Exception as e:
                logger.error(f"Error handling connection: {e}")
            finally:
                conn.close()
                logger.info(f"Connection closed: {addr}")
                
    except Exception as e:
        logger.error(f"DNP3 server error: {e}")

def run_dnp3_server():
    """Start DNP3 server on port 20000"""
    
    if not PYDNP3_AVAILABLE:
        logger.warning("pydnp3 not available, using simple TCP listener")
        logger.warning("For full DNP3 support, install pydnp3: pip install pydnp3")
        run_dnp3_server_simple()
        return
    
    # If pydnp3 is available, use it here
    # Note: pydnp3 installation may have failed during Docker build
    logger.info("pydnp3 library detected, but full implementation not yet configured")
    logger.info("Falling back to simple TCP listener")
    run_dnp3_server_simple()

if __name__ == "__main__":
    run_dnp3_server()


