#!/usr/bin/env python3
"""
OPEL - EtherNet/IP Simulator
Simple EtherNet/IP server for testing and education
Uses pycomm3 library
"""

import logging
from pycomm3 import LogixDriver
import socket
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ethernetip_server():
    """Start EtherNet/IP server on port 2222"""
    
    host = "0.0.0.0"
    port = 2222
    
    try:
        # EtherNet/IP uses both TCP and UDP
        # TCP for explicit messaging
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind((host, port))
        tcp_sock.listen(5)
        
        logger.info(f"EtherNet/IP TCP simulator listening on {host}:{port}")
        
        # UDP for implicit messaging
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind((host, port))
        
        logger.info(f"EtherNet/IP UDP simulator listening on {host}:{port}")
        logger.info("Note: This is a basic implementation. Full EtherNet/IP requires CIP protocol support.")
        
        def handle_tcp():
            while True:
                conn, addr = tcp_sock.accept()
                logger.info(f"TCP connection from {addr}")
                try:
                    data = conn.recv(1024)
                    if data:
                        logger.info(f"Received {len(data)} bytes via TCP")
                        conn.send(b"EtherNet/IP Simulator Response")
                except Exception as e:
                    logger.error(f"TCP error: {e}")
                finally:
                    conn.close()
        
        def handle_udp():
            while True:
                data, addr = udp_sock.recvfrom(1024)
                logger.info(f"Received {len(data)} bytes via UDP from {addr}")
                # Echo back
                udp_sock.sendto(b"EtherNet/IP UDP Response", addr)
        
        # Start handlers in separate threads
        tcp_thread = threading.Thread(target=handle_tcp, daemon=True)
        udp_thread = threading.Thread(target=handle_udp, daemon=True)
        
        tcp_thread.start()
        udp_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"EtherNet/IP server error: {e}")

if __name__ == "__main__":
    run_ethernetip_server()

