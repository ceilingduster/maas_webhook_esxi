# MaaS Webhook power control for VMware ESXi

After an exhausting and brain melting exercise in trying to get MaaS to use virsh against an ESXi box--and failing--this was written.
It's a simple docker container that uses python3, pyvmomi and flask to create a webserver for MaaS's webhook power type.

# Usage in MaaS

```
Stop: http://127.0.0.1:5000/vm/<UUIDHERE>/stop
Start: http://127.0.0.1:5000/vm/<UUIDHERE>/start
Status: http://127.0.0.1:5000/vm/<UUIDHERE>/status
```

# Docker Compose

Edit the docker compose and add your environment variables for your ESXi box and run ```with docker compose up -d```.

# But how do I get UUID's?

Edit list.py, add credentials and:
```
python3 list.py
```
