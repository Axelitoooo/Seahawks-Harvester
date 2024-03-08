import subprocess
import requests
import time


def check_for_updates(github_repo):
    api_url = f"https://api.github.com/repos/{github_repo}/commits"
    response = requests.get(api_url)
    commits = response.json()
    return commits


def pull_changes():
    subprocess.run(["git", "pull"], check=True)


def main():
    github_repo = "Axelitoooo/Seahawks-Harvester"
    last_sha = None

    while True:
        commits = check_for_updates(github_repo)

        if commits and (last_sha is None or commits[0]['sha'] != last_sha):
            print("Des modifications ont été détectées. Voulez-vous mettre à jour ? [y/n]")
            choice = input()

            if choice.lower() == 'y':
                pull_changes()
                print("Mise à jour effectuée.")
                last_sha = commits[0]['sha']
            else:
                print("Mise à jour ignorée.")

        time.sleep(600)  # Vérifier les mises à jour toutes les 10 minutes


if __name__ == "__main__":
    main()
