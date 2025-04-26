import os
import sys
import time
import platform
import subprocess
import winreg as reg
import tkinter as tk
from tkinter import messagebox, ttk

# Define valid taskbar positions
POSITIONS = {
    "Bottom": "03",
    "Left": "00",
    "Top": "01",
    "Right": "02"
}

# Function to detect Windows version
def is_windows_11():
    try:
        version = platform.version().split('.')
        build_number = int(version[2])
        return build_number >= 22000  # Windows 11 starts at build 22000
    except Exception:
        return False

# Function to restart explorer
def restart_explorer():
    subprocess.call(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.Popen("explorer.exe")

# Function to change taskbar position
def set_taskbar_position(position):
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3"
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_path, 0, reg.KEY_SET_VALUE | reg.KEY_QUERY_VALUE)

        # Read current value
        value, _ = reg.QueryValueEx(reg_key, "Settings")
        data = bytearray(value)

        # Change taskbar position byte
        data[12] = int(POSITIONS[position], 16)

        # Write back modified value
        reg.SetValueEx(reg_key, "Settings", 0, reg.REG_BINARY, bytes(data))

        reg.CloseKey(reg_key)

        restart_explorer()

        messagebox.showinfo("Success", f"Taskbar moved to {position} successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to change taskbar position:\n{e}")

# GUI setup
def run_gui():
    root = tk.Tk()
    root.title("TaskbarTweak-Win")
    root.geometry("400x250")
    root.resizable(False, False)

    # Title Label
    title = ttk.Label(root, text="TaskbarTweak-Win", font=("Segoe UI", 18, "bold"))
    title.pack(pady=10)

    # Info
    ttk.Label(root, text="Select where you want your taskbar to appear:", font=("Segoe UI", 11)).pack(pady=5)

    # Dropdown for positions
    selected = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=selected, state="readonly", font=("Segoe UI", 11))
    dropdown['values'] = list(POSITIONS.keys())
    dropdown.current(0)
    dropdown.pack(pady=10)

    # Apply button
    def on_apply():
        pos = selected.get()
        set_taskbar_position(pos)

    apply_btn = ttk.Button(root, text="Apply", command=on_apply)
    apply_btn.pack(pady=20)

    # Version Info
    version_label = ttk.Label(root, text=f"Running on {'Windows 11' if is_windows_11() else 'Windows 10'}", font=("Segoe UI", 9, "italic"))
    version_label.pack(side="bottom", pady=5)

    root.mainloop()

if __name__ == "__main__":
    if os.name != "nt":
        print("This script is only for Windows.")
        sys.exit()

    run_gui()
