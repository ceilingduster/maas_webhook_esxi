from flask import Flask, request, jsonify
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import os

app = Flask(__name__)

# ESXi Credentials
ESXI_HOST = os.getenv('ESXI_HOST', '127.0.0.1')
ESXI_USER = os.getenv('ESXI_USER', 'root')
ESXI_PASSWORD = os.getenv('ESXI_PASSWORD', 'password')

# Disable SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def connect_esxi():
    """Establishes a connection to the ESXi host."""
    return SmartConnect(host=ESXI_HOST, user=ESXI_USER, pwd=ESXI_PASSWORD, sslContext=context)

def get_vm_by_uuid(uuid):
    """Fetches VM object by UUID."""
    si = connect_esxi()
    content = si.RetrieveContent()

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            vm_list = child.vmFolder.childEntity
            for vm in vm_list:
                if vm.config.instanceUuid == uuid:
                    return vm
    Disconnect(si)
    return None

@app.route('/vm/<uuid>/status', methods=['GET'])
def get_vm_status(uuid):
    """Returns 'running' or 'stopped' based on the VM's power state."""
    vm = get_vm_by_uuid(uuid)
    if vm:
        power_state = "running" if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn else "stopped"
        return jsonify({"uuid": uuid, "status": power_state})
    return jsonify({"error": "VM not found"}), 404

@app.route('/vm/<uuid>/start', methods=['POST'])
def start_vm(uuid):
    """Starts the VM by UUID."""
    system_id = request.headers.get("System_id")  # Case-sensitive header
    vm = get_vm_by_uuid(uuid)

    if vm:
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            return jsonify({"uuid": uuid, "status": "running", "system_id": system_id})

        vm.PowerOn()
        return jsonify({"uuid": uuid, "status": "running", "system_id": system_id})
    
    return jsonify({"error": "VM not found"}), 404

@app.route('/vm/<uuid>/stop', methods=['POST'])
def stop_vm(uuid):
    """Stops the VM by UUID."""
    system_id = request.headers.get("System_id")  # Case-sensitive header
    vm = get_vm_by_uuid(uuid)

    if vm:
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
            return jsonify({"uuid": uuid, "status": "stopped", "system_id": system_id})

        vm.PowerOff()
        return jsonify({"uuid": uuid, "status": "stopped", "system_id": system_id})
    
    return jsonify({"error": "VM not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
