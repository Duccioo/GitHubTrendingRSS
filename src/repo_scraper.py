# Importa le librerie necessarie
import requests
from datetime import datetime, timedelta
import os
import json
import base64  # Per decodificare il contenuto del README
from telegraph import Telegraph  # Importa Telegraph
from markdown import markdown  # Importa Markdown per conversione a HTML
from bs4 import BeautifulSoup  # Importa BeautifulSoup


# --- Inizializzazione Telegraph ---
telegraph = None
if telegraph is None:
    try:
        telegraph = Telegraph()
        account_info = telegraph.create_account(short_name="GitHubTrendingReader")
        new_token = account_info.get("access_token")
        print(f"Creato nuovo account Telegraph.")
        print(
            f"*** IMPORTANTE: Aggiungi questa riga al tuo file .env per le prossime esecuzioni: ***"
        )
        print(f"TELEGRAPH_ACCESS_TOKEN={new_token}")
        TELEGRAPH_ACCESS_TOKEN = new_token
    except Exception as e:
        print(f"Errore critico: Impossibile creare un account Telegraph: {e}")
        telegraph = None


# --- Funzioni Helper ---


def get_readme_content(repo_full_name, headers):
    """Recupera e decodifica il contenuto del README.md da un repository."""
    if "/" not in repo_full_name:
        print(f"Nome repository non valido per API: {repo_full_name}")
        return None
    owner, repo_name = repo_full_name.split("/", 1)
    possible_readme_names = ["README.md", "README"]
    for readme_name in possible_readme_names:
        readme_url = (
            f"https://api.github.com/repos/{owner}/{repo_name}/contents/{readme_name}"
        )
        try:
            response = requests.get(readme_url, headers=headers, timeout=10)
            response.raise_for_status()
            content_base64 = response.json().get("content")
            if content_base64:
                decoded_content = base64.b64decode(content_base64).decode("utf-8")
                print(f"  > README ({readme_name}) trovato per {repo_full_name}")
                return decoded_content
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                continue
            else:
                print(
                    f"  > Errore HTTP nel recuperare {readme_name} per {repo_full_name}: {e}"
                )
                return None
        except requests.exceptions.RequestException as e:
            print(
                f"  > Errore di rete nel recuperare {readme_name} per {repo_full_name}: {e}"
            )
            return None
        except Exception as e:
            print(
                f"  > Errore generico nel processare {readme_name} per {repo_full_name}: {e}"
            )
            return None

    print(f"  > Nessun README trovato per {repo_full_name}")
    return None


def create_telegraph_page_from_markdown(title, markdown_content):
    """
    Crea una pagina Telegraph dal contenuto Markdown,
    preservando le immagini e rimuovendo i tag non supportati come <div>.
    """
    if not telegraph or not markdown_content:
        return None
    try:
        # 1. Converti Markdown in HTML
        raw_html_content = markdown(
            markdown_content, extensions=["extra", "codehilite"]
        )  # Usa estensioni per una migliore conversione

        # 2. Pulisci l'HTML usando BeautifulSoup
        # Usare 'lxml' è generalmente più veloce e robusto, ma 'html.parser' è built-in
        soup = BeautifulSoup(raw_html_content, "lxml")

        # Rimuovi i tag <div> mantenendo il loro contenuto
        tag_not_supported = [
            "div",
            "style",
            "body",
            "html",
            "h1",
            "h2",
            "h3",
            "picture",
            "span",
            "table",
        ]
        for tag in tag_not_supported:
            for unsupported_tag in soup.find_all(tag):
                # Sostituisce il tag non supportato con il suo contenuto
                unsupported_tag.unwrap()

        # Ottieni l'HTML pulito come stringa. BeautifulSoup si occupa della codifica.
        cleaned_html_content = str(soup)

        # 3. Crea la pagina Telegraph con l'HTML pulito
        response = telegraph.create_page(
            title=title,
            html_content=cleaned_html_content,  # Usa l'HTML pulito
            author_name="GitHub Trending Bot",
        )
        return response["url"]
    except ImportError:
        print("Errore: Le librerie 'BeautifulSoup' e/o 'lxml' non sono installate.")
        print("Esegui: pip install beautifulsoup4 lxml")
        # Fallback: prova a creare la pagina con l'HTML grezzo (potrebbe fallire o renderizzare male)
        try:
            print("  > Tentativo di fallback con HTML grezzo (potrebbe fallire)...")
            response = telegraph.create_page(
                title=title,
                html_content=raw_html_content,  # Usa HTML non pulito
                author_name="GitHub Trending Bot",
            )
            return response["url"]
        except Exception as fallback_e:
            print(
                f"  > Errore anche nel fallback con HTML grezzo per '{title}': {fallback_e}"
            )
            return None
    except Exception as e:
        # Gestisce errori da BeautifulSoup o Telegraph API
        print(
            f"  > Errore nella creazione/pulizia della pagina Telegraph per '{title}': {e}"
        )
        return None


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
            print("Attenzione: Trovato repository senza 'full_name', saltato.")
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
                repo.get("license", {}).get("name", "No license")
                if repo.get("license")
                else "No license"
            ),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "owner": {
                "name": repo.get("owner", {}).get("login", ""),
                "avatar_url": repo.get("owner", {}).get("avatar_url", ""),
            },
            "telegraph_url": None,
        }

        if telegraph:
            readme_markdown = get_readme_content(repo_full_name, headers)
            if readme_markdown:
                telegraph_page_url = create_telegraph_page_from_markdown(
                    title=f"README - {repo_full_name}",
                    markdown_content=readme_markdown,
                )
                if telegraph_page_url:
                    repo_data["telegraph_url"] = telegraph_page_url
        else:
            print("Skipping Telegraph page creation (Telegraph not initialized).")

        organized_data.append(repo_data)

    return organized_data


def get_trending_repositories(
    language=None, since="daily", limit=20, headers=None, recently_trending=False
):
    """
    Recupera le repository di tendenza su GitHub
    """
    query = "stars:>50"

    if language:
        query += f" language:{language}"

    date_cutoff = None
    if since == "weekly":
        date_cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif since == "monthly":
        date_cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    elif since == "daily":
        date_cutoff = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if recently_trending:
        query += f" pushed:>{date_cutoff}"
    else:
        query += f" created:>{date_cutoff}"

    sort = "stars"
    order = "desc"

    url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={limit}"

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta API per i repository: {e}")
        return []


def main():
    GITHUB_TOKEN = os.getenv("REPO_GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}

    if GITHUB_TOKEN:
        print("Token GitHub trovato. Le richieste API saranno autenticate.")
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    else:
        print(
            "Attenzione: Token GitHub non trovato! Le richieste API potrebbero essere limitate."
            " Il recupero dei README potrebbe fallire."
        )

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    limit_repos = 4
    print(f"\nRecupero max {limit_repos} repository più popolari (monthly)...")
    trending_repos = get_trending_repositories(
        since="monthly", limit=limit_repos, headers=headers
    )
    print(f"Recuperate {len(trending_repos)} repository.")

    print(f"\nRecupero max {limit_repos} repository recentemente popolari (weekly)...")
    recent_trending_repos = get_trending_repositories(
        since="weekly", limit=limit_repos, headers=headers, recently_trending=True
    )
    print(f"Recuperate {len(recent_trending_repos)} repository.")

    print("\nInizio estrazione dati e creazione pagine Telegraph...")
    organized_trending_repos = extract_repo_data(trending_repos, headers)
    organized_recent_trending_repos = extract_repo_data(recent_trending_repos, headers)
    print("\nEstrazione dati e creazione pagine Telegraph completata.")

    trending_json_path = os.path.join(data_dir, "trending_repos.json")
    with open(trending_json_path, "w", encoding="utf-8") as file:
        json.dump(organized_trending_repos, file, ensure_ascii=False, indent=2)
        print(f"Dati salvati in {trending_json_path}")

    recent_trending_json_path = os.path.join(data_dir, "recently_trending_repos.json")
    with open(recent_trending_json_path, "w", encoding="utf-8") as file:
        json.dump(organized_recent_trending_repos, file, ensure_ascii=False, indent=2)
        print(f"Dati salvati in {recent_trending_json_path}")

    print("\n--- Esempi ---")
    if organized_trending_repos:
        print("\nEsempio di repository popolare in generale:")
        organized_repo = organized_trending_repos[0]
        print(f"  Nome: {organized_repo['name']}")
        print(f"  URL: {organized_repo['url']}")
        print(f"  Descrizione: {organized_repo['description']}")
        print(f"  Stelle: {organized_repo['stars']}")
        print(
            f"  Pagina Telegraph README: {organized_repo.get('telegraph_url', 'Non creata/Errore')}"
        )

    if organized_recent_trending_repos:
        print("\nEsempio di repository recentemente popolare:")
        example_repo = next(
            (
                repo
                for repo in organized_recent_trending_repos
                if repo.get("telegraph_url")
            ),
            None,
        )
        if not example_repo and organized_recent_trending_repos:
            example_repo = organized_recent_trending_repos[0]

        if example_repo:
            print(f"  Nome: {example_repo['name']}")
            print(f"  URL: {example_repo['url']}")
            print(f"  Descrizione: {example_repo['description']}")
            print(f"  Stelle: {example_repo['stars']}")
            print(
                f"  Pagina Telegraph README: {example_repo.get('telegraph_url', 'Non creata/Errore')}"
            )
        else:
            print("  Nessun repository recentemente popolare trovato.")


if __name__ == "__main__":
    main()
