# Importa le librerie necessarie
import requests
from datetime import datetime, timedelta
import os
import json
import base64  # Per decodificare il contenuto del README
import logging  # Aggiunto import


# --- Funzione Principale di Estrazione ---


def extract_repo_data(repos, headers):
    """
    Estrae i dati essenziali dalle repository e crea pagine Telegraph per i README.

    Parameters:
    repos (list): Lista di repository dall'API GitHub
    headers (dict): Headers per l'autenticazione API (necessari per README)

    Returns:
    list: Lista di dizionari con i dati organizzati, incluso telegraph_url
    """
    organized_data = []

    for repo in repos:
        repo_full_name = repo.get("full_name")
        if not repo_full_name:
            logging.warning("Attenzione: Trovato repository senza 'full_name', saltato.")
            continue

        repo_data = {
            "name": repo_full_name,
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "No description provided"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", "Not specified"),
            "topics": repo.get("topics", []),
            "license": (
                repo.get("license", {}).get("name", "No license") if repo.get("license") else "No license"
            ),
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
    """
    minimum_stars = 10
    query = f"stars:>={minimum_stars}"

    if language:
        query += f" language:{language}"

    # Imposta il cutoff della data solo per i periodi temporali
    date_cutoff = None
    if since == "daily":
        date_cutoff = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif since == "weekly":
        date_cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif since == "monthly":
        date_cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    # Aggiungi il filtro per data solo se 'since' non è 'all-time'
    # Usiamo 'pushed' per riflettere l'attività recente, non la data di creazione
    if since != "all-time" and date_cutoff:
        query += f" pushed:>{date_cutoff}"

    sort = "stars"
    order = "desc"

    url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={limit}"
    try:
        response = requests.get(url, headers=headers, timeout=15)

        response.raise_for_status()

        data = response.json()

        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Errore durante la richiesta API per i repository: {e}")
        return []
    except Exception as e:
        logging.exception(f"Errore imprevisto durante il recupero dei repository: {e}")
        return []


