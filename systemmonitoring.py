import psutil
import time
import os
from datetime import datetime

# Function to monitor CPU core usage
def cpu_usage_per_core():
    try:
        core_usage = psutil.cpu_percent(interval=1, percpu=True)
        return core_usage
    except Exception as e:
        print(f"Error getting CPU core usage: {e}")
        return []

# Function to get CPU temperature (if supported)
def cpu_temperature():
    try:
        # Not all systems support temperature monitoring
        temperatures = psutil.sensors_temperatures()
        if "coretemp" in temperatures:
            temp = temperatures["coretemp"][0].current
            return temp
        else:
            return None
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
        return None
def most_cpu_intensive_process():
    try:
        # List of processes sorted by CPU usage
        processes = [(p.info["cpu_percent"], p.info["name"], p.info["pid"]) for p in psutil.process_iter(['cpu_percent', 'name', 'pid'])]
        processes.sort(reverse=True, key=lambda x: x[0])  # Sort by CPU usage
        
        # Filter out System Idle Process (PID: 0)
        processes = [p for p in processes if p[1] != "System Idle Process"]
        
        return processes[0] if processes else None
    except Exception as e:
        print(f"Error getting process info: {e}")
        return None


# Function to log CPU usage
def log_cpu_usage(cpu_usage):
    try:
        with open("cpu_usage_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - CPU Usage: {cpu_usage}%\n")
    except Exception as e:
        print(f"Error logging CPU usage: {e}")

# Function to send alerts if CPU usage exceeds a threshold
def alert_high_cpu_usage(cpu_usage, threshold=80):
    if cpu_usage > threshold:
        print(f"ALERT: CPU usage is high: {cpu_usage}%")
        # You can also implement additional alert mechanisms here like email or SMS.

# Main system monitoring loop
def advanced_system_monitor():
    try:
        while True:
            # Get overall CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Get CPU usage per core
            core_usage = cpu_usage_per_core()
            
            # Get CPU temperature
            temp = cpu_temperature()
            
            # Get the most CPU-intensive process
            process = most_cpu_intensive_process()

            # Print system stats
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal screen
            print(f"Overall CPU Usage: {cpu_usage}%")
            if core_usage:
                print("CPU Core Usage:")
                for i, usage in enumerate(core_usage):
                    print(f"  Core {i}: {usage}%")
            if temp is not None:
                print(f"CPU Temperature: {temp}°C")
            if process:
                print(f"Most CPU-Intensive Process: {process[1]} (PID: {process[2]}) - {process[0]}% CPU usage")
            
            # Log CPU usage
            log_cpu_usage(cpu_usage)
            
            # Alert if CPU usage exceeds threshold
            alert_high_cpu_usage(cpu_usage)
            
            print("=" * 50)
            time.sleep(1)  # Update every second

    except KeyboardInterrupt:
        print("🛑System monitoring stopped.")

# Run the advanced system monitor
advanced_system_monitor()
