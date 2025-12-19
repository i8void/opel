#!/usr/bin/env python3
"""
OPEL - BACnet/IP Simulator
Simple BACnet/IP server for testing and education
Uses bacpypes library - configured for unicast mode (Docker-friendly)
"""

import logging
import socket

# Try to import bacpypes
try:
    from bacpypes.core import run, deferred, enable_sleeping
    from bacpypes.app import BIPSimpleApplication
    from bacpypes.local.device import LocalDeviceObject
    from bacpypes.service.device import WhoIsIAmServices
    from bacpypes.primitivedata import ObjectIdentifier
    from bacpypes.constructeddata import ArrayOf
    BACNET_AVAILABLE = True
except ImportError:
    BACNET_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bacnet_server_simple():
    """Simple BACnet UDP listener (fallback)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 47808))
    logger.info("Simple BACnet UDP listener started on port 47808")
    
    while True:
        data, addr = sock.recvfrom(1024)
        logger.info(f"Received {len(data)} bytes from {addr}")

def run_bacnet_server():
    """Start BACnet/IP server on port 47808"""
    
    if not BACNET_AVAILABLE:
        logger.warning("bacpypes not available, using simple UDP listener")
        run_bacnet_server_simple()
        return
    
    try:
        # Create local device object first
        # ObjectIdentifier can be created as ('device', 1001) or ObjectIdentifier('device', 1001)
        try:
            obj_id = ObjectIdentifier('device', 1001)
        except (TypeError, ValueError):
            # Try tuple format if ObjectIdentifier constructor fails
            obj_id = ('device', 1001)
        
        local_device = LocalDeviceObject(
            objectName='OPEL-BACnet-Simulator',
            objectIdentifier=obj_id,
            maxApduLengthAccepted=1024,
            segmentationSupported='segmentedBoth',
            vendorIdentifier=999,
        )
        
        # Create BACnet application with proper arguments
        # BIPSimpleApplication expects (address, port) tuple and local device
        try:
            app = BIPSimpleApplication(
                ('0.0.0.0', 47808),  # (address, port) tuple
                local_device
            )
        except TypeError:
            # Try alternative initialization if the above fails
            app = BIPSimpleApplication(
                '0.0.0.0',  # address
                47808,      # port
                local_device
            )
        
        logger.info("Starting BACnet/IP simulator on port 47808 (UDP)")
        logger.info("Note: Configured for unicast mode (Docker-friendly)")
        logger.info("Multicast device discovery may not work in Docker bridge networks")
        logger.info(f"Device Name: {local_device.objectName}")
        logger.info(f"Device ID: {local_device.objectIdentifier}")
        
        # Run the application
        run()
        
    except Exception as e:
        logger.error(f"BACnet server error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        logger.info("Falling back to simple UDP listener...")
        run_bacnet_server_simple()

if __name__ == "__main__":
    run_bacnet_server()

