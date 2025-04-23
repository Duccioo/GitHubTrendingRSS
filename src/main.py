# Importa le librerie necessarie
import os
import time
from datetime import datetime
import json
from dotenv import load_dotenv
import pathlib
import logging  # Aggiunto import

# ----
load_dotenv(".env")

# ---- Configurazione del logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# ----

from repo_scraper import get_trending_repositories, extract_repo_data
from gen_feed import create_rss_feed
import website
from config import TIMEOUT, LANGUAGE, PERIOD


def generate_all_feeds(limit=30):
    """
    Generates Atom feeds for all languages and time periods
    and saves them in the 'feeds' folder.
    """
    # Definisci l'URL base per i tuoi feed
    base_feed_url = "https://duccioo.github.io/GitHubTrendingRSS/"  # Modifica se necessario

    # Define supported languages
    languages = LANGUAGE  # Importa le lingue da config.py
    languages.sort()  # Ordina alfabeticamente

    # Define time periods
    periods = PERIOD

    # Create feeds folder if it doesn't exist
    feeds_dir = pathlib.Path("feeds")  # Definisci la directory dei feed
    feeds_dir.mkdir(parents=True, exist_ok=True)  # Crea la directory se non esiste

    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    data_dir = pathlib.Path(data_dir)  # Definisci la directory dei dati
    data_dir.mkdir(parents=True, exist_ok=True)  # Crea la directory se non esiste

    count = 0
    errors = 0

    # Recupera il token GitHub una sola volta
    GITHUB_TOKEN = os.getenv("REPO_GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        logging.info("Token GitHub trovato. Le richieste API saranno autenticate.")
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    else:
        logging.warning(
            "Attenzione: Token GitHub non trovato! Le richieste API potrebbero essere limitate."
            " Il recupero dei README potrebbe fallire."
        )

    # Generate feed for each language and period combination
    for language in languages:
        for period in periods:
            try:
                logging.info(f"Generazione feed per {language} ({period})...")

                # Use None for 'All Languages' and convert appropriately for 'Unknown languages'
                lang_param = None if language == "Unknow Languages" else language
                if language == "Unknown languages":
                    lang_param = None  # Tratta come All per ora
                elif language == "All Languages":
                    lang_param = "all"

                # Get repositories
                repos = get_trending_repositories(
                    language=lang_param, since=period, limit=limit, headers=headers
                )

                if repos:
                    # Estrai dati e crea pagine Telegraph (passa headers)
                    organized_repos = extract_repo_data(repos, headers)

                    # Costruisci l'URL e il nome del file specifici
                    # Crea filename sicuro
                    lang_filename_part = (
                        language.replace(" ", "_").replace("#", "sharp").replace("+", "plus").lower()
                    )

                    period_lower = period.lower()
                    filename = feeds_dir / f"{lang_filename_part}_{period_lower}.xml"
                    feed_url = f"{base_feed_url}{filename.name}"  # Aggiorna URL

                    trending_json_path = data_dir / f"{lang_filename_part}_{period_lower}.json"

                    with open(trending_json_path, "w", encoding="utf-8") as file:
                        json.dump(organized_repos, file, ensure_ascii=False, indent=2)
                        logging.info(f"Dati salvati in {trending_json_path}")

                    # Generate RSS feed
                    feed_title = f"GitHub Trending - {language} ({period.capitalize()})"  # Capitalize period
                    feed_description = (
                        f"Repository più popolari su GitHub in {language} nel periodo {period.lower()}"
                    )
                    rss_feed = create_rss_feed(
                        organized_repos,
                        feed_url=feed_url,
                        title=feed_title,
                        description=feed_description,
                    )

                    # Save RSS feed
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(rss_feed)

                    count += 1
                    logging.info(f"Feed salvato: {filename}")

                    # Add a small pause to avoid too many API requests
                    time.sleep(TIMEOUT / 1000)  # Converti millisecondi in secondi
                else:
                    logging.info(f"Nessun repository trovato per {language} ({period})")
                    # Non incrementare errors se è normale non trovare repo (es. linguaggi rari)

            except Exception as e:
                logging.exception(f"Errore durante la generazione per {language} ({period}): {e}")
                errors += 1

    logging.info(f"\nCompletato! Feed generati: {count}, Errori: {errors}")
    return count, errors


def main():
    # Definisci la directory di output per il sito (es. la root del progetto)
    output_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )  # Directory principale del progetto

    # --- Carica i dati dei repository popolari ---
    popular_repos_data = []
    # Definisci il percorso del file JSON dei repo popolari
    data_dir = os.path.join(output_directory, "data")
    trending_json_file = os.path.join(data_dir, "trending_repos.json")

    try:
        with open(trending_json_file, "r", encoding="utf-8") as f:
            all_repos = json.load(f)
            # Ordina per stelle decrescenti
            popular_repos_data = sorted(all_repos, key=lambda x: x.get("stars", 0), reverse=True)
        logging.info(
            f"Caricati {len(popular_repos_data)} repository da {trending_json_file} per gli esempi del sito."
        )
    except FileNotFoundError:
        logging.warning(
            f"Attenzione: File {trending_json_file} non trovato. La sezione dei repository popolari nel sito sarà vuota."
        )
    except json.JSONDecodeError:
        logging.error(f"Errore: Impossibile decodificare il JSON da {trending_json_file}.")
    except Exception as e:
        logging.exception(f"Errore imprevisto durante il caricamento di {trending_json_file}: {e}")

    # --- Genera tutti i feed ---
    generate_all_feeds()

    # --- Genera e salva il sito web ---
    logging.info("\nGenerazione sito web...")
    # Passa i dati caricati alla funzione di generazione del sito
    html_content = website.generate_website()

    # Salva il sito web nel file index.html nella directory di output principale
    if website.save_website(html_content, output_dir=output_directory, filename="index.html"):
        logging.info(f"Sito web generato e salvato come {os.path.join(output_directory, 'index.html')}")
    else:
        logging.error("Errore durante il salvataggio del sito web.")


if __name__ == "__main__":
    logging.info(f"Esecuzione iniziata: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    logging.info(f"Esecuzione completata: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
