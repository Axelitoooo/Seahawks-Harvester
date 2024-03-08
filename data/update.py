import subprocess
import requests
import time

# Assurez-vous de remplacer 'your_personal_access_token' par votre token d'accès personnel GitHub
github_token = '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'


def check_for_updates(github_repo):
    api_url = f"https://api.github.com/repos/{github_repo}/commits?per_page=1"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(api_url, headers=headers)
    print(f"Vérification des mises à jour pour {github_repo}")
    if response.status_code == 200:
        commits = response.json()
        if commits and isinstance(commits, list) and len(commits) > 0:
            last_commit_sha = commits[0]['sha']
            print(f"Dernier commit SHA: {last_commit_sha}")
            return last_commit_sha
        else:
            print("Pas de nouveaux commits trouvés.")
    else:
        print(f"Erreur lors de la récupération des commits. Statut HTTP: {response.status_code}")
    return None


def pull_changes():
    subprocess.run(["git", "pull"], check=True)


def main():
    github_repo = "Axelitoooo/Seahawks-Harvester"
    last_sha = None

    while True:
        current_sha = check_for_updates(github_repo)

        if current_sha and current_sha != last_sha:
            print("Des modifications ont été détectées. Voulez-vous mettre à jour ? [y/n]")
            choice = input()

            if choice.lower() == 'y':
                pull_changes()
                print("Mise à jour effectuée.")
                last_sha = current_sha
            else:
                print("Mise à jour ignorée.")
        else:
            print("Aucune mise à jour disponible ou erreur lors de la vérification des mises à jour.")

        time.sleep(60)  # Vérifier les mises à jour toutes les 10 minutes


if __name__ == "__main__":
    main()
