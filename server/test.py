import os
import psutil
import platform
import time
from subprocess import PIPE, Popen

# List of suspicious process names (keyloggers, clipboard spies, screen capture)
suspicious_processes = [
    "keylogger", "xinput", "xev", "getkeys", "screenrecord", "screencapture",
    "python", "pyhook", "pyxhook", "clipboard", "copyq", "vnc", "teamviewer",
    "remote"
]

def check_suspicious_processes():
    found_suspicious = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            if any(sus in proc_name for sus in suspicious_processes):
                found_suspicious.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return found_suspicious

def check_windows_hooks():
    # Detect keylogging hooks on Windows (basic)
    if platform.system() == "Windows":
        print("Checking for keyloggers in Windows...")
        # Here we can use ctypes or PowerShell to detect keylogger hooks (simplified)
        try:
            hooks = os.popen('powershell Get-Process -Name "KeyLogger"').read()
            if hooks:
                print("Warning: Keylogger found!")
            else:
                print("No keylogger hooks detected.")
        except Exception as e:
            print(f"Error checking hooks: {e}")

def check_linux_screenspy():
    # Detect screen capturing on Linux using x11 tools
    if platform.system() == "Linux":
        print("Checking for screen capture tools in Linux...")
        cmd = "xwininfo -tree -root | grep 'screenshot'"
        result = Popen(cmd, shell=True, stdout=PIPE).stdout.read().decode()
        if result:
            print("Warning: Screenshot tool might be active.")
        else:
            print("No active screenshot tools detected.")

def check_clipboard_access():
    # Monitor clipboard access (basic detection)
    print("Monitoring clipboard access (Press Ctrl+C to stop)...")
    if platform.system() == "Windows":
        from win32clipboard import OpenClipboard, GetClipboardData, CloseClipboard
    else:
        import subprocess

    previous_clipboard = ""
    while True:
        try:
            # Linux command to access clipboard
            if platform.system() == "Linux":
                clipboard_content = subprocess.check_output(["xclip", "-o"]).decode("utf-8")
            elif platform.system() == "Windows":
                OpenClipboard()
                clipboard_content = GetClipboardData()
                CloseClipboard()

            if clipboard_content != previous_clipboard:
                print(f"Clipboard changed: {clipboard_content}")
                previous_clipboard = clipboard_content

            time.sleep(2)  # Adjust frequency to detect more often
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")

if __name__ == "__main__":
    system_os = platform.system()
    print(f"Running detection on: {system_os}")

    suspicious_procs = check_suspicious_processes()
    if suspicious_procs:
        print(f"Suspicious processes detected: {suspicious_procs}")
    else:
        print("No suspicious processes found.")

    if system_os == "Windows":
        check_windows_hooks()
    elif system_os == "Linux":
        check_linux_screenspy()

    # Monitor clipboard access (optional, can stop with Ctrl+C)
    try:
        check_clipboard_access()
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped.")
