# --- Author : ABHISHEK SATPATHY (https://abhisat.com)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import time
import os
import json
import subprocess
import sys
import signal
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

SCHEDULE_FILE = "schedules.json"
LOG_FILE = "log.txt"

scheduler = BackgroundScheduler()
scheduler.start()

tray_icon = None
root = tk.Tk()
root.title("Task Scheduler")

# --- Task Execution Function ---
def run_script(filepath):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Executed: {filepath}\n"

        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_entry)

        if filepath.endswith('.sh'):
            subprocess.call(['bash', filepath])
        else:
            subprocess.Popen(filepath, shell=True)
    except Exception as e:
        error_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {str(e)}\n"
        with open(LOG_FILE, "a") as log_file:
            log_file.write(error_log)

# --- Scheduling Function ---
def schedule_task(frequency, dt, filepath):
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M")
    if frequency == "Daily":
        trigger = CronTrigger(hour=dt.hour, minute=dt.minute)
    elif frequency == "Weekly":
        trigger = CronTrigger(day_of_week=dt.weekday(), hour=dt.hour, minute=dt.minute)
    elif frequency == "Monthly":
        trigger = CronTrigger(day=dt.day, hour=dt.hour, minute=dt.minute)
    else:
        return

    job_id = f"{filepath}_{frequency}"
    scheduler.add_job(run_script, trigger, args=[filepath], id=job_id, replace_existing=True)

# --- Save Schedules to File ---
def save_schedule_to_file(frequency, dt, filepath):
    data = {"frequency": frequency, "datetime": dt, "filepath": filepath}
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)

    with open(SCHEDULE_FILE, "w") as f:
        json.dump(existing, f, indent=2)

# --- Load Schedules from File ---
def load_and_reschedule():
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r") as f:
                data = json.load(f)
            for job in data:
                if all(k in job for k in ("frequency", "datetime", "filepath")):
                    try:
                        datetime.strptime(job["datetime"], "%Y-%m-%d %H:%M")
                        schedule_task(job["frequency"], job["datetime"], job["filepath"])
                    except Exception as e:
                        with open(LOG_FILE, "a") as log_file:
                            log_file.write(f"[{datetime.now()}] Skipped invalid job: {job}, Reason: {e}\n")
        except Exception as e:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"[{datetime.now()}] Failed to load jobs: {e}\n")

# --- Tray & GUI Actions ---
def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Script Files", "*.exe *.sh *.bat *.py")])
    if path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, path)

def minimize_to_tray():
    global tray_icon
    root.withdraw()

    def on_exit(icon, item):
        try:
            if scheduler.running:
                scheduler.shutdown(wait=False)
            icon.visible = False
            icon.stop()
            root.quit()
            os.kill(os.getpid(), signal.SIGTERM)  # Force kill to stop background process
        except Exception as e:
            with open(LOG_FILE, "a") as log:
                log.write(f"[{datetime.now()}] Exit error: {e}\n")
            os._exit(0)

    def show_window(icon, item):
        root.after(0, root.deiconify)
        icon.visible = False
        icon.stop()

    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill='blue')

    tray_icon = Icon("Task Scheduler", image, menu=Menu(
        MenuItem("Open", show_window),
        MenuItem("Exit", on_exit)
    ))

    threading.Thread(target=tray_icon.run, daemon=True).start()

def on_run():
    freq = freq_var.get().strip()
    datetime_input = date_entry.get().strip()
    file_path = file_entry.get().strip()

    if not freq or not datetime_input or not file_path:
        messagebox.showerror("Missing Input", "All fields are required.")
        return

    try:
        datetime.strptime(datetime_input, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Invalid Input", "Date & Time format must be YYYY-MM-DD HH:MM")
        return

    schedule_task(freq, datetime_input, file_path)
    save_schedule_to_file(freq, datetime_input, file_path)
    messagebox.showinfo("Scheduled", "Task has been scheduled. The app will now minimize to tray.")
    minimize_to_tray()

# --- GUI Layout ---
ttk.Label(root, text="Select Frequency:").grid(row=0, column=0, padx=10, pady=5)
freq_var = tk.StringVar()
freq_dropdown = ttk.Combobox(root, textvariable=freq_var, values=["Daily", "Weekly", "Monthly"], state="readonly")
freq_dropdown.grid(row=0, column=1, padx=10, pady=5)
freq_dropdown.current(0)

ttk.Label(root, text="Date & Time (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
date_entry = ttk.Entry(root, width=30)
date_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Select Script File:").grid(row=2, column=0, padx=10, pady=5)
file_entry = ttk.Entry(root, width=30)
file_entry.grid(row=2, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_file).grid(row=2, column=2, padx=5)

ttk.Button(root, text="Run", command=on_run).grid(row=3, column=1, pady=15)

# --- Load Schedules on Start ---
load_and_reschedule()

# --- Start GUI ---
root.mainloop()

# --- Author : ABHISHEK SATPATHY (https://abhisat.com)