#!/usr/bin/python3
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# ESXi Connection Details
ESXI_HOST = "172.16.0.1"
ESXI_USER = "root"
ESXI_PASSWORD = "passw0rd"

# Disable SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def get_vm_uuids():
    # Connect to ESXi
    si = SmartConnect(host=ESXI_HOST, user=ESXI_USER, pwd=ESXI_PASSWORD, sslContext=context)
    content = si.RetrieveContent()

    # Get all VMs
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            vm_list = child.vmFolder.childEntity
            for vm in vm_list:
                print(f"VM Name: {vm.name} | UUID: {vm.config.instanceUuid}")

    # Disconnect
    Disconnect(si)

if __name__ == "__main__":
    get_vm_uuids()
