import subprocess
import socket
import re

print("\n🌐 NetSpy - LAN Device Scanner")
print("=" * 60)

# Get hostname
hostname = socket.gethostname()

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
finally:
    s.close()

# Default router IP
router_ip = ".".join(local_ip.split(".")[:3]) + ".1"


# Function to get MAC address from ARP table
def get_mac(ip):
    try:
        output = subprocess.check_output("arp -a", shell=True).decode()

        for line in output.splitlines():
            if ip in line:
                mac_match = re.search(
                    r"([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}",
                    line
                )

                if mac_match:
                    return mac_match.group()

    except:
        pass

    return "Unknown"


print("\n🖥 YOUR DEVICE")
print("-" * 60)
print(f"Device Name : {hostname}")
print(f"IP Address  : {local_ip}")

print("\n📡 ROUTER INFORMATION")
print("-" * 60)
print(f"Router IP   : {router_ip}")
print(f"MAC Address : {get_mac(router_ip)}")
print("Status      : Online")

network = ".".join(local_ip.split(".")[:3])

print("\n🔍 Scanning Network...")
print("=" * 60)

devices = []

for i in range(1, 255):

    ip = f"{network}.{i}"

    result = subprocess.run(
        ["ping", "-n", "1", "-w", "100", ip],
        capture_output=True,
        text=True
    )

    if "TTL=" in result.stdout:

        if ip == local_ip:
            continue

        if ip == router_ip:
            continue

        try:
            device_name = socket.gethostbyaddr(ip)[0]
        except:
            device_name = "Unknown Device"

        devices.append({
            "name": device_name,
            "ip": ip,
            "mac": get_mac(ip),
            "status": "Online"
        })

print("\n📋 DETECTED DEVICES")
print("=" * 60)

if len(devices) == 0:
    print("No active devices found.")

else:

    for count, device in enumerate(devices, start=1):

        print(f"\nDevice #{count}")
        print(f"Name        : {device['name']}")
        print(f"IP Address  : {device['ip']}")
        print(f"MAC Address : {device['mac']}")
        print(f"Status      : {device['status']}")
        print("-" * 60)

print(f"\n✅ Total Devices Found : {len(devices)}")
print("=" * 60)