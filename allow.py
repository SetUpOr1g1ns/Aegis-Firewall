import tkinter as tk
from tkinter import ttk
import subprocess
import ipaddress
import sqlite3
from datetime import datetime


# === Event Registration ===
def log(msg):
    try:
        with open("Resources\\Data\\logs.txt", "a", encoding="utf-8") as event:
            date = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            event.write(f"{date} {msg}\n")
    except Exception as e:
        print(f"💀​ Error while registering event: {msg}. Context: {e}")


# === Add IP to Allowlist ===
def dbAllowIP(address):
    try:
        conn = sqlite3.connect("Resources\\Data\\ip.db")
        cur = conn.cursor()
        cur.execute('DELETE FROM blocked_ips WHERE ip = ?', (address,))
        cur.execute('INSERT OR REPLACE INTO allowed_ips (ip) VALUES (?)', (address,))
        conn.commit()
        conn.close()
        log(f"✅​​ Successfully allowed IP ({address})")
    except Exception as e:
        log(f"❌ Unable to add IP ({address}) to allowed_ips in the database. Context: {e}")


# === "allow.py" GUI Window ===
def allow_menu():
    def valid(address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False


    def repeated(address):
        try:
            conn = sqlite3.connect("Resources\\Data\\ip.db")
            cur = conn.cursor()
            cur.execute("SELECT ip FROM allowed_ips WHERE ip = ?", (address,))
            exists = cur.fetchone()
            conn.close()
            return exists is not None
        except Exception as e:
            log(f"❌ Unable to check if IP ({address}) was repeated. Context: {e}")
            return False


    def allow_and_unblock(address):
        try:
            rule = f"BLOCKED_IP_{address.replace('.', '_')}"
            subprocess.run(f'netsh advfirewall firewall delete rule name="{rule}_IN"', shell=True)
            subprocess.run(f'netsh advfirewall firewall delete rule name="{rule}_OUT"', shell=True)

            rule = f"ALLOWED_IP_{address.replace('.', '_')}"
            cmd_in = f'netsh advfirewall firewall add rule name="{rule}_IN" interface=any dir=in action=allow remoteip={address}'
            cmd_out = f'netsh advfirewall firewall add rule name="{rule}_OUT" interface=any dir=out action=allow remoteip={address}'

            subprocess.run(cmd_in, shell=True)
            subprocess.run(cmd_out, shell=True)
            log(f"✅​ Successfully added Firewall rules to IP ({address}).")
        except Exception as e:
            log(f"⚠️ Unable to add Firewall rules to IP ({address}). Context: {e}")


    def allow_ip():
        ip = entrybox.get().strip()
        message = ""
        try:
            if ip:
                if valid(ip) and repeated(ip):
                    message = f"IP {ip} was already allowed."
                elif valid(ip) and not repeated(ip):
                    dbAllowIP(ip)
                    message = f"IP {ip} allowed."
                    log(f"✅​ Successfully allowed manually added IP ({ip})")
                else:
                    message = "Invalid IP format."

            for i in list_ips.curselection():
                sel_ip = list_ips.get(i).strip()
                if valid(sel_ip) and not repeated(sel_ip):
                    dbAllowIP(sel_ip)
                    message += f"\nIP ({sel_ip}) unblocked and allowed."
                    log(f"✅​ Successfully allowed via listbox IP ({sel_ip})")
                    conn = sqlite3.connect("Resources\\Data\\ip.db")
                    cur = conn.cursor()
                    cur.execute('DELETE FROM blocked_ips WHERE ip = ?', (sel_ip,))
                    conn.commit()
                    conn.close()

            lbl_msg.config(text=message)
        except Exception as e:
            log(f"❌ Unable to allow IP ({ip}). Context: {e}")


    # === GUI ===
    root = tk.Toplevel()
    root.title("Allow Connection Menu")
    root.geometry("450x350")
    root.resizable(False, False)
    root.config(bg="#172445")

    frame = tk.Frame(root, bg="#172445")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=320)

    tk.Label(frame, text="Allow IP:", font=("Arial", 14, "bold"), fg="white", bg="#172445").pack(pady=10)

    cont = tk.Frame(frame, bg="#172445")
    cont.pack(fill="both", expand=True, padx=20)

    left = tk.Frame(cont, bg="#172445")
    left.pack(side="left", fill="both", expand=True)

    frame_in = tk.Frame(left, bg="#172445")
    frame_in.pack(pady=10)

    tk.Label(frame_in, text="Input an IP:", fg="white", bg="#172445").pack()
    entrybox = ttk.Entry(frame_in, width=25, justify="center")
    entrybox.pack(pady=5)

    ttk.Button(left, text="Allow IP", command=allow_ip).pack(pady=5)

    lbl_msg = tk.Label(left, text="", fg="cyan", bg="#172445", wraplength=200, justify="center")
    lbl_msg.pack(pady=10)

    right = tk.Frame(cont, bg="#172445")
    right.pack(side="right", fill="both", expand=True, padx=(20, 0))

    tk.Label(right, text="Blocked IPs:", fg="white", bg="#172445").pack()

    frame_list = tk.Frame(right, bg="#172445")
    frame_list.pack(fill="both", expand=True, pady=(15, 40))

    list_ips = tk.Listbox(frame_list, width=23, height=8, selectmode="extended")
    list_ips.pack(side="left", fill="both", expand=True, padx=(0, 10))

    scroll = ttk.Scrollbar(frame_list, orient="vertical", command=list_ips.yview)
    scroll.pack(side="right", fill="y")
    list_ips.config(yscrollcommand=scroll.set)

    # Display blocked IPs in the listbox
    def load_blocked_ips():
        try:
            conn = sqlite3.connect("Resources\\Data\\ip.db")
            cur = conn.cursor()
            cur.execute("SELECT ip FROM blocked_ips")
            datos = [row[0] for row in cur.fetchall()]
            conn.close()
            return datos
        except Exception as e:
            log(f"❌ Unable to display blocked IPs: {e}")
            return []

    for ip in load_blocked_ips():
        list_ips.insert(tk.END, ip)

    root.mainloop()