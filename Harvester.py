import json
import os
from tkinter import Tk, Button, Text, messagebox
import nmap
import threading
import subprocess
import requests
from datetime import datetime

# Lire le token d'accès depuis une variable d'environnement
github_token = os.getenv('GITHUB_TOKEN')

# Définition de last_sha au niveau global
last_sha = None


def check_for_updates(github_repo):
    api_url = f"https://api.github.com/repos/{github_repo}/commits?per_page=1"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        if commits and isinstance(commits, list) and len(commits) > 0:
            last_commit_sha = commits[0]['sha']
            if last_commit_sha != last_sha:
                return last_commit_sha
    return None


def pull_changes():
    subprocess.run(["git", "stash", "push", "data"], check=True)  # Ignore le.data
    subprocess.run(["git", "pull"], check=True)
    subprocess.run(["git", "stash", "pop"], check=True)


def update_application():
    github_repo = "Axelitoooo/Seahawks-Harvester"
    current_sha = check_for_updates(github_repo)
    if current_sha and current_sha != last_sha:
        if messagebox.askyesno("Mise à jour disponible",
                               "Des modifications ont été détectées. Voulez-vous mettre à jour ?"):
            pull_changes()
            messagebox.showinfo("Mise à jour", "L'application a été mise à jour.")


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
    sorted_hosts = sorted(hosts, key=lambda x: x[0])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename_prefix = "scan_automated" if automated else "scan"
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    file_path = os.path.join(data_folder, f"{filename_prefix}_{timestamp}.json")
    with open(file_path, 'w') as file:
        json.dump(sorted_hosts, file, indent=4)
    if not automated:
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

scan_btn = Button(app, text="Scan Network", command=lambda: threading.Thread(target=launch_scan_and_save).start())
scan_btn.pack()

update_btn = Button(app, text="Vérifier et appliquer les mises à jour", command=update_application)
update_btn.pack()

app.mainloop()
