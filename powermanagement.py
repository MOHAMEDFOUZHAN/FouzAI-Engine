import psutil
import pyttsx3
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Adjust speed

def speak(text):
    """Convert text to speech"""
    print(text)  # Display text output
    engine.say(text)
    engine.runAndWait()

def battery_status():
    """Check battery percentage and status"""
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected."

    percent = battery.percent
    charging = "Charging" if battery.power_plugged else "Not Charging"
    time_left = battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Calculating..."
    
    return f"Battery at {percent} percent. Status: {charging}. Estimated time left: {time_left} minutes."

def power_consumption():
    """Get top power-consuming apps"""
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            cpu_usage = proc.info['cpu_percent']
            if cpu_usage > 0:  # Ignore idle processes
                processes.append((proc.info['name'], cpu_usage))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes.sort(key=lambda x: x[1], reverse=True)  # Sort by CPU usage
    return processes[:5]  # Return top 5 power-consuming apps

if __name__ == "__main__":
    # Speak battery status
    speak(battery_status())

    # Speak power-consuming apps
    speak("Here are the top power-consuming applications:")
    
    for name, cpu in power_consumption():
        speak(f"{name} is using {cpu} percent CPU.")
