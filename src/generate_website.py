import os
import json
from datetime import datetime


def load_repositories(file_path):
    """
    Carica i dati delle repository dal file JSON
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Errore nel caricamento del file {file_path}: {e}")
        return []


def get_language_class(language):
    """
    Genera una classe CSS per il colore del linguaggio
    """
    if not language or language == "no language":
        return "language-default"

    # Rimuovi spazi e caratteri speciali per la classe CSS
    return f"language-{language.replace(' ', '').replace('#', 'Sharp').replace('+', 'p')}"


def generate_repo_html(repo):
    """
    Genera l'HTML per una singola repository
    """
    language_class = get_language_class(repo.get("language"))
    language_display = repo.get("language", "No language")
    if language_display == "no language":
        language_display = "No language"

    return f"""
    <div class="repo-card">
        <h3 class="repo-name"><a href="{repo.get('url', '#')}" target="_blank">{repo.get('name', 'Unknown')}</a></h3>
        <p class="repo-description">{repo.get('description', 'No description')}</p>
        <div class="repo-meta">
            <span><span class="language-dot {language_class}"></span> {language_display}</span>
            <span>⭐ {repo.get('stars', 0)}</span>
            <span>🍴 {repo.get('forks', 0)}</span>
        </div>
    </div>
    """


def generate_rss_links_html(rss_directory):
    """
    Genera l'HTML per i link ai feed RSS
    """
    html = ""

    if os.path.exists(rss_directory):
        rss_files = [f for f in os.listdir(rss_directory) if f.endswith(".xml")]

        for rss_file in rss_files:
            feed_name = os.path.splitext(rss_file)[0].replace("_", " ").title()
            feed_url = f"rss/{rss_file}"
            html += f'<li><a href="{feed_url}" class="rss-button" target="_blank">{feed_name}</a></li>\n'

    return html


def generate_website():
    """
    Genera la pagina web HTML
    """
    # Percorsi dei file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(base_dir, "data")
    docs_dir = os.path.join(base_dir, "docs")
    rss_dir = os.path.join(base_dir, "rss")
    template_path = os.path.join(current_dir, "templates", "index_template.html")

    # Assicurati che la directory docs esista
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # Carica i dati delle repository
    popular_repos = load_repositories(os.path.join(data_dir, "trending_repos.json"))
    trending_repos = load_repositories(os.path.join(data_dir, "recently_trending_repos.json"))

    # Verifica se i file esistono e contengono dati
    if not popular_repos:
        popular_repos = []  # Usa una lista vuota se non ci sono dati

    if not trending_repos:
        trending_repos = []  # Usa una lista vuota se non ci sono dati

    # Leggi il template HTML
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
    except Exception as e:
        print(f"Errore nel caricamento del template: {e}")
        template_content = "<html><body><h1>GitHub Trending Repository</h1></body></html>"

    # Genera l'HTML per le repository popolari
    popular_repos_html = "".join(generate_repo_html(repo) for repo in popular_repos[:20])

    # Genera l'HTML per le repository in tendenza
    trending_repos_html = "".join(generate_repo_html(repo) for repo in trending_repos[:20])

    # Genera l'HTML per i link RSS
    rss_links_html = generate_rss_links_html(rss_dir)

    # Data di aggiornamento
    updated_date = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Sostituisci i segnaposto nel template
    html_content = template_content.replace("<!-- POPULAR_REPOSITORIES -->", popular_repos_html)
    html_content = html_content.replace("<!-- TRENDING_REPOSITORIES -->", trending_repos_html)
    html_content = html_content.replace("<!-- RSS_FEEDS -->", rss_links_html)
    html_content = html_content.replace("<!-- UPDATED_DATE -->", updated_date)

    # Scrivi il file HTML
    output_path = os.path.join(docs_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Pagina web generata con successo: {output_path}")


if __name__ == "__main__":
    generate_website()
