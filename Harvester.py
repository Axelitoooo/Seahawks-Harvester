import json
import os
from tkinter import Tk, Button, Text, messagebox
from datetime import datetime
import nmap
import threading


def scan_network():
    nm = nmap.PortScanner()
    nm.scan('192.168.1.1/24', arguments='-sn')
    hosts = []
    for host in nm.all_hosts():
        try:
            mac_address = nm[host]['addresses'].get('mac', 'MAC non trouvée')
            host_name = nm[host].hostname()
            hosts.append((host, host_name, mac_address))
        except KeyError:
            hosts.append((host, 'Informations non disponibles', 'MAC non trouvée'))
    return hosts


def save_results(hosts, automated=False):
    # Sort hosts by IP address
    sorted_hosts = sorted(hosts, key=lambda x: x[0])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename_prefix = "scan_automated" if automated else "scan"
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    file_path = os.path.join(data_folder, f"{filename_prefix}_{timestamp}.json")
    with open(file_path, 'w') as file:
        json.dump(sorted_hosts, file, indent=4)
    if 'display' in globals():
        messagebox.showinfo("Sauvegarde réussie",
                            f"Les résultats du scan ont été sauvegardés en JSON sous {file_path}.")


def launch_scan_and_save(automated=False):
    hosts = scan_network()
    save_results(hosts, automated)


def scheduled_scan():
    launch_scan_and_save(automated=True)
    threading.Timer(3600, scheduled_scan).start()


# Lancer un scan automatique au démarrage
threading.Timer(1, scheduled_scan).start()

# Interface graphique Tkinter
app = Tk()
app.title("Network Scanner")
app.geometry("400x300")

display = Text(app, height=15)
display.pack()

scan_btn = Button(app, text="Scan Network",
                  command=lambda: threading.Thread(target=lambda: launch_scan_and_save(automated=False)).start())
scan_btn.pack()

save_btn = Button(app, text="Sauvegarder les Résultats", state='disabled')
save_btn.pack()

app.mainloop()
