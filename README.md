# 🛡️ Aegis Firewall

## 📖 Main Description

Aegis Firewall is a Python-based GUI tool for managing Windows Firewall rules. It allows users to block and allow IP addresses, store them in a database, synchronize with online blacklists, and keep a detailed log of all events.  

---

## 🚀 Installation & Instructions

You can set up and run the project in Windows by:

1. Downloading the project.  
2. Executing `setup.ps1` in the `Tools` folder.
3. Running `main.py` with **admin privileges**.
4. Right click on the Aegis Firewall system tray icon and click on **Open GUI**.

*Note that this was primarily intended for use **only on Windows systems***

---

## 🧰 Repair Tools & Troubleshooting

This section is for common issues and how to fix them.  

- If the GUI does not open, check that all image files (`bg.png`, `icon.png`) exist.
- If firewall rules do not apply, make sure the app is run as administrator.  
- If the database is corrupted, run `repair_db` in the `Tools` folder.
- For other errors, try uninstalling and reinstalling. To keep your database, copy it from `Resources\Data` and replace it after reinstalling.

*Note that this was primarily intended for use **only on Windows systems***

---

## 🔎 Inner Workings & Explanations

### 🔧 Main breakdown of files and their location

- **main.py** → Handles the main GUI and tray icon and contacts the rest of files.
- **allow.py** → Manages connection permission to specified IP addresses
- **block.py** → Manages the denial of access to connections to specific IP addresses
- **update.py** → Handles the syncing with online blacklists.  

### 🖥️ Explanation

Running `main.py` with administrator privileges initiates the Aegis Firewall application. It first launches the system tray icon using the `pystray` library, allowing the program to run quietly in the background. Once the user selects "Open GUI" from the tray menu, the graphical interface is started in a separate thread using `tkinter` for the GUI components and `threading` to avoid interference between the tray icon and the GUI.

The GUI itself provides four main options: Allow, Block, Online Blacklist, and Exit. Each of these options is handled by separate Python scripts located in the `Resources\Functions` directory:

The Allow and Block features open a small window where users can input an IP address they wish to either permit or block. These actions create corresponding rules in the Windows Firewall and also classify the IP address in the local database `Resources\Data\ip.db` using SQL queries. The window includes a user-friendly interface with an input box that validates the input using the `valid(address)` function and checks for duplicates of that IP with the `repeated(address)` function. Additionally, a listbox displays blocked or allowed IPs from the database, allowing users to select and reclassify them if needed. If the input is invalid, a warning message is shown, and any errors or actions encountered during the process are logged in `Resources\Data\logs.txt`.

The Online Blacklist feature automatically updates the Windows Firewall with the latest malicious IPs from Feodo Tracker’s blocklist. To maintain accuracy and prevent false positives, the application removes the previous blocklist and replaces it with the most recent version each time the feature is used.

The Exit button in the GUI closes the graphical interface but leaves the system tray icon active, allowing users to reopen the GUI at any time. To fully exit the application, users can right-click the tray icon and select "Exit."

### ⚙️ Performance

- **RAM Usage**: Under 40 MB
- **CPU Usage**: ~0% on average (except during blacklist updates)
- **Compressed Images**: Image size has been reduced by an average of 40.5%.
- **Optimization Potential**: Can be further enhanced using tools like `cython` .

---

## 🛠️ Libraries & Technologies Used

List of the libraries, frameworks, and tools used to build the project:

- **Python 3.8+**  
- **Windows’ built-in firewall (netsh advfirewall)**
- **Tkinter** – GUI framework for building the graphical interface  
- **PIL / Pillow** – Image handling and manipulation  
- **Pystray** – System tray icon integration  
- **Threading** – Running concurrent tasks (e.g. GUI and tray icon)  
- **SQLite3** – Local database for storing IP classifications  
- **Subprocess** – Executing Windows Firewall commands  
- **Ipaddress** – Validating and parsing IP addresses  
- **Datetime** – Handling timestamps and log entries  
- **CSV** – Reading and writing structured data files  
- **Requests** – Fetching online resources (e.g. Feodo Tracker blocklist)  

---

## 📂 Project Structure

A short overview of folders and their purpose:

AegisFirewall/\
├── Resources/\
│ ├── Assets/---------# Contains graphic files such as bg.png and icon.png\
│ ├── Data/-----------# Database and logs: ip.db and logs.txt\
│ └── Functions/----- # Functional scripts: allow.py, block.py, update.py\
├── Tools/-------------# Maintenance utilities: setup.ps1 and repair_db.py\
├── main.py-----------# Main program file\
└── README.md------# Markdown documentation
