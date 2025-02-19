import psutil
import socket
import time
from colorama import Fore, init

# Initialize colorama for Windows support
init(autoreset=True)

previous_received = 0
previous_sent = 0
start_time = time.time()

def network_activity():
    global previous_received, previous_sent, start_time
    
    # Get network IO counters
    net = psutil.net_io_counters()
    
    # Calculate current speeds (Mbps)
    bytes_received = net.bytes_recv
    bytes_sent = net.bytes_sent
    
    # Calculate the difference in received and sent bytes
    received_speed = (bytes_received - previous_received) / (time.time() - start_time) / 1024 / 1024  # in Mbps
    sent_speed = (bytes_sent - previous_sent) / (time.time() - start_time) / 1024 / 1024  # in Mbps

    # Update previous values
    previous_received = bytes_received
    previous_sent = bytes_sent
    start_time = time.time()

    # Format the output
    network_data = f"""
    📶 **Network Activity Report**:
    -----------------------------------------
    🌐 **Current Download Speed**: {received_speed:.2f} Mbps
        - The rate at which data is being received from the internet.
    🌐 **Current Upload Speed**: {sent_speed:.2f} Mbps
        - The rate at which data is being sent to the internet.
    
    💻 **Total Data Sent**: {bytes_sent / (1024 ** 2):.2f} MB
        - Total amount of data that has been uploaded since the last reset.
    💻 **Total Data Received**: {bytes_received / (1024 ** 2):.2f} MB
        - Total amount of data that has been downloaded since the last reset.
    
    🖧 **Network Interfaces**:
    ---------------------------
    """
    
    # Get network interfaces and their status
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                status = 'Active' if psutil.net_if_stats()[interface].isup else 'Inactive'
                network_data += f"  🌐 **Interface**: {interface} | IP: {addr.address} | Status: {status}\n"

    return network_data.strip()

if __name__ == "__main__":
    print("Fetching your network activity details...\n")
    print(network_activity())  # Print the network activity once
