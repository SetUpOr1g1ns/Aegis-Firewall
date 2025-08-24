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


# === Add IP to Blocklist ===
def dbBlockIP(address):
    try:
        conn = sqlite3.connect("Resources\\Data\\ip.db")
        cur = conn.cursor()
        cur.execute('DELETE FROM allowed_ips WHERE ip = ?', (address,))
        cur.execute('INSERT OR REPLACE INTO blocked_ips (ip) VALUES (?)', (address,))
        conn.commit()
        conn.close()
        log(f"✅​​ Successfully blocked IP ({address})")
    except Exception as e:
        log(f"❌ Unable to add IP ({address}) to blocked_ips in the database. Context: {e}")


# === "block.py" GUI Window ===
def block_menu():
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
            cur.execute("SELECT ip FROM blocked_ips WHERE ip = ?", (address,))
            existe = cur.fetchone()
            conn.close()
            return existe is not None
        except Exception as e:
            log(f"❌ Unable to check if IP ({address}) was repeated. Context: {e}")
            return False

    def block_and_deny(address):
        try:
            regla = f"ALLOWED_IP_{address.replace('.', '_')}"
            subprocess.run(f'netsh advfirewall firewall delete rule name="{regla}_IN"', shell=True)
            subprocess.run(f'netsh advfirewall firewall delete rule name="{regla}_OUT"', shell=True)

            regla = f"BLOCKED_IP_{address.replace('.', '_')}"
            cmd_in = f'netsh advfirewall firewall add rule name="{regla}_IN" interface=any dir=in action=block remoteip={address}'
            cmd_out = f'netsh advfirewall firewall add rule name="{regla}_OUT" interface=any dir=out action=block remoteip={address}'

            subprocess.run(cmd_in, shell=True)
            subprocess.run(cmd_out, shell=True)
            log(f"✅​ Successfully added Firewall rules to IP ({address}).")
        except Exception as e:
            log(f"⚠️ Unable to add Firewall rules to Ip ({address}). Context: {e}")

    def block_ip():
        ip = entrybox.get().strip()
        message = ""
        try:
            if ip:
                if valid(ip) and repeated(ip):
                    message = f"IP {ip} was already blocked."
                elif valid(ip) and not repeated(ip):
                    dbBlockIP(ip)
                    message = f"IP {ip} blocked."
                    log(f"✅​ Successfully blocked manually added IP ({ip})")
                    block_and_deny(ip)
                else:
                    message = "Invalid IP format."

            for i in list_ips.curselection():
                sel_ip = list_ips.get(i).strip()
                if valid(sel_ip) and not repeated(sel_ip):
                    dbBlockIP(sel_ip)
                    message += f"\nIP ({sel_ip}) blocked."
                    log(f"✅​ Successfully blocked via listbox IP ({sel_ip})")
                    conn = sqlite3.connect("Resources\\Data\\ip.db")
                    cur = conn.cursor()
                    cur.execute('DELETE FROM allowed_ips WHERE ip = ?', (sel_ip))
                    conn.commit()
                    conn.close()
                    block_and_deny(ip)

            lbl_msg.config(text=message)
        except Exception as e:
            log(f"❌ Unable to block IP ({ip}). Context: {e}")


    # === GUI ===
    root = tk.Toplevel()
    root.title("Block Connection Menu")
    root.geometry("450x350")
    root.resizable(False, False)
    root.config(bg="#172445")

    frame = tk.Frame(root, bg="#172445")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=320)

    tk.Label(frame, text="Block IP:", font=("Arial", 14, "bold"), fg="white", bg="#172445").pack(pady=10)

    cont = tk.Frame(frame, bg="#172445")
    cont.pack(fill="both", expand=True, padx=20)

    left = tk.Frame(cont, bg="#172445")
    left.pack(side="left", fill="both", expand=True)

    frame_in = tk.Frame(left, bg="#172445")
    frame_in.pack(pady=10)

    tk.Label(frame_in, text="Input an IP:", fg="white", bg="#172445").pack()
    entrybox = ttk.Entry(frame_in, width=25, justify="center")
    entrybox.pack(pady=5)

    tk.Button(left,text="Block IP", command=block_ip, width=15, bg="#1f2e5a", fg="white", relief="flat", cursor="hand2").pack(pady=5)

    lbl_msg = tk.Label(left, text="", fg="cyan", bg="#172445", wraplength=200, justify="center")
    lbl_msg.pack(pady=10)

    right = tk.Frame(cont, bg="#172445")
    right.pack(side="right", fill="both", expand=True, padx=(20, 0))

    tk.Label(right, text="Allowed IPs:", fg="white", bg="#172445").pack()

    frame_list = tk.Frame(right, bg="#172445")
    frame_list.pack(fill="both", expand=True, pady=(15, 40))

    list_ips = tk.Listbox(frame_list, width=23, height=8, selectmode="extended", bg="#1f2e5a", fg="white", relief="flat")
    list_ips.pack(side="left", fill="both", expand=True, padx=(0, 10))

    scroll = ttk.Scrollbar(frame_list, orient="vertical", command=list_ips.yview)
    scroll.pack(side="right", fill="y")
    list_ips.config(yscrollcommand=scroll.set)

    # Display allowed IPs in the listbox
    def load_allowed_ips():
        try:
            conn = sqlite3.connect("Resources\\Data\\ip.db")
            cur = conn.cursor()
            cur.execute("SELECT ip FROM allowed_ips")
            datos = [row[0] for row in cur.fetchall()]
            conn.close()
            return datos
        except Exception as e:
            log(f"❌ Unable to display allowed IPs: {e}")
            return []

    for ip in load_allowed_ips():
        list_ips.insert(tk.END, ip)

    root.mainloop()
