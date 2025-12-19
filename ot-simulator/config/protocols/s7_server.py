#!/usr/bin/env python3
"""
OPEL - S7 (Siemens) Simulator
Simple S7 server using SNAP7 library
"""

import logging
import socket

# Try to import snap7
try:
    import snap7
    try:
        import snap7.snap7types
        SNAP7_TYPES_AVAILABLE = True
    except ImportError:
        try:
            from snap7 import snap7types
            SNAP7_TYPES_AVAILABLE = True
        except ImportError:
            SNAP7_TYPES_AVAILABLE = False
    SNAP7_AVAILABLE = True
except ImportError:
    SNAP7_AVAILABLE = False
    SNAP7_TYPES_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_s7_server_simple():
    """Simple S7 TCP listener (fallback)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 102))
    sock.listen(5)
    
    logger.info("Simple S7 TCP listener started on port 102")
    
    while True:
        conn, addr = sock.accept()
        logger.info(f"S7 connection from {addr}")
        try:
            data = conn.recv(1024)
            if data:
                logger.info(f"Received {len(data)} bytes")
                # Basic S7-like response (ISO-on-TCP connection response)
                conn.send(b'\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc0\x01\x0a\xc1\x02\x01\x00\xc2\x02\x01\x02')
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            conn.close()

def run_s7_server():
    """Start S7 server on port 102"""
    
    if not SNAP7_AVAILABLE:
        logger.warning("snap7 not available, using simple TCP listener")
        run_s7_server_simple()
        return
    
    try:
        # Create S7 server
        server = snap7.server.Server()
        
        # Configure server
        server.create()
        
        # Set server parameters
        if SNAP7_TYPES_AVAILABLE:
            try:
                server.set_param(snap7.snap7types.S7_Params.LocalPort, 102)
                server.set_param(snap7.snap7types.S7_Params.WorkInterval, 50)
                server.set_param(snap7.snap7types.S7_Params.MaxClients, 8)
            except (AttributeError, NameError):
                # Try alternative import
                from snap7 import snap7types
                server.set_param(snap7types.S7_Params.LocalPort, 102)
                server.set_param(snap7types.S7_Params.WorkInterval, 50)
                server.set_param(snap7types.S7_Params.MaxClients, 8)
        else:
            # Try setting port directly if types not available
            logger.warning("snap7types not available, using default parameters")
        
        # Start server
        server.start()
        
        logger.info("S7 (Siemens) simulator started on port 102")
        logger.info("Server is ready to accept connections")
        
        # Keep server running
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down S7 server...")
            server.stop()
            server.destroy()
            
    except Exception as e:
        logger.error(f"S7 server error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        logger.info("Falling back to simple TCP listener...")
        run_s7_server_simple()

if __name__ == "__main__":
    run_s7_server()

