#!/usr/bin/env python3
"""
OPEL - IEC 104 Simulator
Simple IEC 104 server for testing and education
Note: Full IEC 104 implementation requires specialized libraries
"""

import socket
import logging
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_iec104_server():
    """Start IEC 104 server on port 2404"""
    
    host = "0.0.0.0"
    port = 2404
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        
        logger.info(f"IEC 104 simulator listening on {host}:{port}")
        logger.info("Note: This is a basic TCP listener. Full IEC 104 protocol requires IEC 61850 libraries.")
        
        while True:
            conn, addr = sock.accept()
            logger.info(f"Connection from {addr}")
            
            try:
                # IEC 104 start frame (0x68 0x04 0x07 0x00 0x00 0x00)
                start_frame = b'\x68\x04\x07\x00\x00\x00'
                conn.send(start_frame)
                logger.info("Sent IEC 104 start frame")
                
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    logger.info(f"Received {len(data)} bytes: {data.hex()}")
                    
                    # Basic response (IEC 104 format)
                    # This is simplified - real IEC 104 requires proper ASDU encoding
                    response = b'\x68\x04\x01\x00\x00\x00'
                    conn.send(response)
                    
            except Exception as e:
                logger.error(f"Error handling connection: {e}")
            finally:
                conn.close()
                logger.info(f"Connection closed: {addr}")
                
    except Exception as e:
        logger.error(f"IEC 104 server error: {e}")

if __name__ == "__main__":
    run_iec104_server()


