# 🗓️ Simple Script Scheduler Tool

A lightweight and user-friendly Python-based GUI tool to schedule the execution of `.exe`, `.sh`, `.bat`, or `.py` script files at recurring intervals (Daily, Weekly, Monthly). The tool runs quietly in the system tray and continues execution until the system is restarted or the app is explicitly exited.

---

## 🚀 Features

- ✅ **Simple GUI** with dropdowns and file browser
- ✅ Schedule tasks with:
  - Daily
  - Weekly
  - Monthly frequencies
- ✅ Automatically minimizes to the system tray after scheduling
- ✅ Reopens GUI from system tray icon
- ✅ Runs scripts in the background without blocking the UI
- ✅ Logs execution and errors to a `log.txt` file
- ✅ Remembers previously scheduled tasks on restart
- ✅ Gracefully exits and shuts down background processes

---

## 🖥️ Screenshot

![image](https://github.com/user-attachments/assets/d849c5bd-dbcf-4d4b-9be9-808a020c9a17)


---

## 🛠️ Installation

### 🔹 Prerequisites

- Python 3.7+
- `pip install -r requirements.txt`

### 🔹 Required Packages

```bash
pip install apscheduler pystray pillow
```
## 🧑‍💻 Usage
- Run the Python script:
    python task_scheduler.py
- Select:
    - Frequency (Daily, Weekly, Monthly)
    - Date & Time (in YYYY-MM-DD HH:MM format)
    - Script File to execute
- Click Run → The app will schedule the task and minimize to the tray.
- Use the tray icon to:
    - 🔁 Open: Restore the GUI
    - ❌ Exit: Shut down the app completely

## 📝 File Structure

📦 TaskScheduler/
 ┣ 📜 task_scheduler.py        # Main application script
 ┣ 📜 schedules.json           # Auto-created file to store scheduled jobs
 ┣ 📜 log.txt                  # Auto-created log file for execution/errors
 ┗ 📜 README.md                # This file

## 📌 Notes

- Only one instance should be run at a time.
- Uses apscheduler for background task scheduling.
- Compatible with .exe, .sh, .bat, and .py scripts.
- The tool is designed to stay minimized and non-intrusive.

## 🙌 Author
**Abhishek Satpathy (Voodoo Coder)** - [Abhishek Satpathy](https://abhisat.com)
