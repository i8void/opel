#!/usr/bin/env python3
"""
OPEL - Modbus TCP Simulator
Simple Modbus TCP server for testing and education
"""

import logging
import socket
import threading

# Try to import pymodbus, fallback to simple TCP if not available
try:
    from pymodbus.server import StartTcpServer
    from pymodbus.device import ModbusDeviceIdentification
    from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
    PYMODBUS_AVAILABLE = True
except ImportError:
    try:
        # Try old API
        from pymodbus.server.sync import StartTcpServer
        from pymodbus.device import ModbusDeviceIdentification
        from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
        PYMODBUS_AVAILABLE = True
    except ImportError:
        PYMODBUS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_modbus_server_simple():
    """Simple Modbus TCP listener (fallback)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 502))
    sock.listen(5)
    logger.info("Simple Modbus TCP listener started on port 502")
    
    while True:
        conn, addr = sock.accept()
        logger.info(f"Modbus connection from {addr}")
        try:
            data = conn.recv(1024)
            if data:
                logger.info(f"Received {len(data)} bytes")
                # Basic Modbus response (transaction ID + protocol ID + length + unit ID + function code)
                response = data[:2] + b'\x00\x00\x00\x03' + data[6:7] + b'\x01\x00\x00'
                conn.send(response)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            conn.close()

def run_modbus_server():
    """Start Modbus TCP server on port 502"""
    
    if not PYMODBUS_AVAILABLE:
        logger.warning("pymodbus not available, using simple TCP listener")
        run_modbus_server_simple()
        return
    
    try:
        # Initialize data store
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [17]*100),
            co=ModbusSequentialDataBlock(0, [17]*100),
            hr=ModbusSequentialDataBlock(0, [17]*100),
            ir=ModbusSequentialDataBlock(0, [17]*100)
        )
        
        context = ModbusServerContext(slaves=store, single=True)
        
        # Device identification
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'OPEL'
        identity.ProductCode = 'MODBUS-SIM'
        identity.VendorUrl = 'https://github.com/opel'
        identity.ProductName = 'Modbus TCP Simulator'
        identity.ModelName = 'OPEL-MODBUS-1.0'
        identity.MajorMinorRevision = '1.0.0'
        
        logger.info("Starting Modbus TCP server on port 502...")
        StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))
    except Exception as e:
        logger.error(f"Failed to start pymodbus server: {e}")
        logger.info("Falling back to simple TCP listener...")
        run_modbus_server_simple()

if __name__ == "__main__":
    run_modbus_server()

