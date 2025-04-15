# Importa le librerie necessarie
import requests
import json
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv


# ----
load_dotenv(".env")


def extract_repo_data(repos):
    """
    Estrae i dati essenziali dalle repository

    Parameters:
    repos (list): Lista di repository dall'API GitHub

    Returns:
    list: Lista di dizionari con i dati organizzati
    """
    organized_data = []

    for repo in repos:
        # Estrai i dati essenziali
        repo_data = {
            "name": repo.get("full_name", ""),
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "no description"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", "no language"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "owner": {
                "name": repo.get("owner", {}).get("login", ""),
                "avatar_url": repo.get("owner", {}).get("avatar_url", ""),
            },
        }

        organized_data.append(repo_data)

    return organized_data


def get_trending_repositories(language=None, since="daily", limit=20, headers=None, recently_trending=False):
    """
    Recupera le repository di tendenza su GitHub

    Parameters:
    language (str): Linguaggio di programmazione da filtrare (opzionale)
    since (str): Periodo di tempo ('daily', 'weekly', 'monthly')
    limit (int): Numero massimo di repository da recuperare
    headers (dict): Headers per l'autenticazione nell'API
    recently_trending (bool): Se True, cerca repository che hanno guadagnato popolarità recentemente

    Returns:
    list: Lista delle repository più popolari
    """
    # L'API Search di GitHub è più efficace per questa operazione
    query = "stars:>50"

    if language:
        query += f" language:{language}"

    # Determina il periodo di tempo
    date_cutoff = None
    if since == "weekly":
        date_cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif since == "monthly":
        date_cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    elif since == "daily":
        date_cutoff = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if recently_trending:
        # Cerca repository che hanno avuto un incremento significativo di stelle nel periodo specificato
        sort = "stars"
        # Utilizza il parametro di data per trovare repository che hanno guadagnato stelle recentemente
        query += f" pushed:>{date_cutoff}"
    else:
        # Approccio originale: ordina per stelle totali
        query += f" created:>{date_cutoff}"
        sort = "stars"

    order = "desc"

    # Costruisci l'URL dell'API
    url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={limit}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per HTTP error

        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta API: {e}")
        return []


def main():
    # Configurazione del token di autenticazione GitHub
    # Utilizza una variabile d'ambiente o inserisci direttamente il token
    # (Ma è meglio non includere token direttamente nel codice)

    # Ottieni il token da una variabile d'ambiente
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # Configura gli headers per le richieste API
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

    # Verifica se il token è stato impostato
    if not GITHUB_TOKEN:
        print("Attenzione: Token GitHub non trovato! Le richieste API potrebbero essere limitate.")
        headers = {"Accept": "application/vnd.github.v3+json"}
    else:
        print("Token GitHub trovato. Le richieste API saranno autenticate.")

    # Recupera repository più popolari in generale
    trending_repos = get_trending_repositories(since="weekly", limit=10, headers=headers)
    print(f"Recuperate {len(trending_repos)} repository più popolari in generale")

    # Recupera repository che hanno guadagnato popolarità recentemente
    recent_trending_repos = get_trending_repositories(
        since="daily", limit=5, headers=headers, recently_trending=True
    )
    print(f"Recuperate {len(recent_trending_repos)} repository che hanno guadagnato popolarità recentemente")

    # Mostra un esempio dei dati organizzati per repository popolari in generale
    if trending_repos:
        print("\nEsempio di repository popolare in generale:")
        organized_repo = extract_repo_data([trending_repos[0]])[0]
        print(f"Nome: {organized_repo['name']}")
        print(f"URL: {organized_repo['url']}")
        print(f"Descrizione: {organized_repo['description']}")
        print(f"Stelle: {organized_repo['stars']}")

    # Mostra un esempio dei dati organizzati per repository recentemente popolari
    if recent_trending_repos:
        print("\nEsempio di repository recentemente popolare:")
        organized_repo = extract_repo_data([recent_trending_repos[0]])[0]
        print(f"Nome: {organized_repo['name']}")
        print(f"URL: {organized_repo['url']}")
        print(f"Descrizione: {organized_repo['description']}")
        print(f"Stelle: {organized_repo['stars']}")


if __name__ == "__main__":
    # Esegui la funzione principale
    main()
