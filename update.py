import requests, csv
import subprocess, sqlite3
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
        log(f"✅​​ Successfully blocked IP ({address}) with update.py")
    except Exception as e:
        log(f"❌ Unable to add IP ({address}) to blocked_ips in the database with update.py. Context: {e}")


# === Update Database with New Malware IPs ===
def update_db():
    response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

    rule="netsh advfirewall firewall delete rule name='BadIP'"
    subprocess.run(["Powershell", "-Command", rule])

    mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.splitlines()))
    
    for row in mycsv:
        ip = row[1]
        if ip != "dst_ip":
            rule = "netsh advfirewall firewall add rule name='BadIP' Dir=Out Action=Block RemoteIP=" + ip
            subprocess.run(["Powershell", "-Command", rule])
            rule = "netsh advfirewall firewall add rule name='BadIP' Dir=In Action=Block RemoteIP=" + ip
            subprocess.run(["Powershell", "-Command", rule])
            dbBlockIP(ip)