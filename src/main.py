# Importa le librerie necessarie
import os
import time
from datetime import datetime, timezone, timedelta
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
from config import TIMEOUT, LANGUAGE, PERIOD, FEED_TYPE


def generate_all_feeds(limit=30, max_days=14):
    """
    Generates Atom feeds for all languages and time periods,
    and saves them in the 'feeds' folder.
    Older entries are pruned based on max_days.
    """
    # Definisci l'URL base per i tuoi feed
    base_feed_url = (
        "https://duccioo.github.io/GitHubTrendingRSS/"  # Modifica se necessario
    )

    # Define supported languages, periods, and feed types
    languages = LANGUAGE
    periods = PERIOD
    feed_types = FEED_TYPE
    languages.sort()

    # Create feeds folder if it doesn't exist
    feeds_dir = pathlib.Path("feeds")
    feeds_dir.mkdir(parents=True, exist_ok=True)

    data_dir = pathlib.Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

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
        )

    # Generate feed for each combination
    for language in languages:
        for period in periods:
            for feed_type in feed_types:
                # Condizione per 'last_update': solo per 'All Languages'
                if feed_type == "last_update" and language != "All Languages":
                    continue

                try:
                    logging.info(
                        f"Generazione feed per {language} ({period}, {feed_type})..."
                    )

                    lang_param = "all" if language == "All Languages" else language
                    if language == "Unknown languages":
                        lang_param = None

                    # Get repositories
                    repos = get_trending_repositories(
                        language=lang_param,
                        since=period,
                        limit=limit,
                        headers=headers,
                        feed_type=feed_type,
                    )

                    if not repos:
                        logging.info(
                            f"Nessun repository trovato per {language} ({period}, {feed_type})"
                        )
                        continue

                    current_trending_repos = extract_repo_data(repos, headers)
                    unique_repos = {
                        repo["url"]: repo for repo in current_trending_repos
                    }.values()
                    current_trending_repos = list(unique_repos)

                    # Costruisci il nome del file
                    lang_fn = language.replace(" ", "_").lower()
                    filename_xml = (
                        feeds_dir / f"{lang_fn}_{period.lower()}_{feed_type}.xml"
                    )
                    filename_json = (
                        data_dir / f"{lang_fn}_{period.lower()}_{feed_type}.json"
                    )
                    feed_url = f"{base_feed_url}{filename_xml.name}"

                    final_repos_for_feed = list(current_trending_repos)
                    processed_urls = {repo["url"] for repo in current_trending_repos}

                    if os.path.exists(filename_json):
                        try:
                            with open(filename_json, "r", encoding="utf-8") as f:
                                previous_repos = json.load(f)
                            time_threshold = datetime.now(timezone.utc) - timedelta(
                                days=max_days
                            )
                            added_from_history = 0
                            for repo in previous_repos:
                                if repo["url"] not in processed_urls:
                                    updated_at = datetime.fromisoformat(
                                        repo["updated_at"].replace("Z", "+00:00")
                                    )
                                    if updated_at > time_threshold:
                                        final_repos_for_feed.append(repo)
                                        processed_urls.add(repo["url"])
                                        added_from_history += 1
                            if added_from_history > 0:
                                logging.info(
                                    f"Aggiunti {added_from_history} repository storici."
                                )
                        except (json.JSONDecodeError, KeyError) as e:
                            logging.warning(
                                f"Errore nel processare {filename_json}: {e}"
                            )

                    final_repos_for_feed.sort(key=lambda x: x["stars"], reverse=True)

                    with open(filename_json, "w", encoding="utf-8") as f:
                        json.dump(
                            final_repos_for_feed, f, ensure_ascii=False, indent=2
                        )
                    logging.info(
                        f"Dati salvati in {filename_json} ({len(final_repos_for_feed)} repo)."
                    )

                    # Generate RSS feed
                    type_str = (
                        "Nuovi" if feed_type == "new" else "Aggiornati di recente"
                    )
                    feed_title = f"GitHub Trending - {type_str} in {language} ({period.capitalize()})"
                    feed_description = f"Repository ({type_str}) più popolari in {language} nel periodo {period.lower()}."

                    rss_feed = create_rss_feed(
                        final_repos_for_feed,
                        feed_url=feed_url,
                        title=feed_title,
                        description=feed_description,
                    )

                    with open(filename_xml, "w", encoding="utf-8") as f:
                        f.write(rss_feed)
                    count += 1
                    logging.info(f"Feed salvato: {filename_xml}")

                    time.sleep(TIMEOUT / 1000)

                except Exception as e:
                    logging.exception(
                        f"Errore per {language} ({period}, {feed_type}): {e}"
                    )
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
            popular_repos_data = sorted(
                all_repos, key=lambda x: x.get("stars", 0), reverse=True
            )
        logging.info(
            f"Caricati {len(popular_repos_data)} repository da {trending_json_file} per gli esempi del sito."
        )
    except FileNotFoundError:
        logging.warning(
            f"Attenzione: File {trending_json_file} non trovato. La sezione dei repository popolari nel sito sarà vuota."
        )
    except json.JSONDecodeError:
        logging.error(
            f"Errore: Impossibile decodificare il JSON da {trending_json_file}."
        )
    except Exception as e:
        logging.exception(
            f"Errore imprevisto durante il caricamento di {trending_json_file}: {e}"
        )

    # --- Genera tutti i feed ---
    generate_all_feeds()

    # --- Genera e salva il sito web ---
    logging.info("\nGenerazione sito web...")
    # Passa i dati caricati alla funzione di generazione del sito
    html_content = website.generate_website()

    # Salva il sito web nel file index.html nella directory di output principale
    if website.save_website(
        html_content, output_dir=output_directory, filename="index.html"
    ):
        logging.info(
            f"Sito web generato e salvato come {os.path.join(output_directory, 'index.html')}"
        )
    else:
        logging.error("Errore durante il salvataggio del sito web.")


if __name__ == "__main__":
    logging.info(f"Esecuzione iniziata: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    logging.info(
        f"Esecuzione completata: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
