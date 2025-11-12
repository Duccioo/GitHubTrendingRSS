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
from config import TIMEOUT, LANGUAGE, PERIOD


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

    # Define supported languages
    languages = LANGUAGE  # Importa le lingue da config.py
    languages.sort()  # Ordina alfabeticamente

    # Define time periods
    periods = PERIOD

    # Create feeds folder if it doesn't exist
    feeds_dir = pathlib.Path("feeds")  # Definisci la directory dei feed
    feeds_dir.mkdir(parents=True, exist_ok=True)  # Crea la directory se non esiste

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )
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
                    current_trending_repos = extract_repo_data(repos, headers)

                    # --- Inizio logica di de-duplicazione ---
                    # Rimuovi duplicati basati su 'url' mantenendo il primo incontro
                    unique_repos = []
                    seen_urls = set()
                    for repo in current_trending_repos:
                        if "url" in repo and repo["url"] not in seen_urls:
                            unique_repos.append(repo)
                            seen_urls.add(repo["url"])

                    if len(current_trending_repos) > len(unique_repos):
                        logging.info(
                            f"Rimossi {len(current_trending_repos) - len(unique_repos)} duplicati dalla lista dei repository correnti."
                        )

                    current_trending_repos = unique_repos
                    # --- Fine logica di de-duplicazione ---

                    # Costruisci l'URL e il nome del file specifici
                    # Crea filename sicuro
                    lang_filename_part = (
                        language.replace(" ", "_")
                        .replace("#", "sharp")
                        .replace("+", "plus")
                        .lower()
                    )

                    period_lower = period.lower()
                    filename = feeds_dir / f"{lang_filename_part}_{period_lower}.xml"
                    feed_url = f"{base_feed_url}{filename.name}"  # Aggiorna URL

                    trending_json_path = (
                        data_dir / f"{lang_filename_part}_{period_lower}.json"
                    )

                    # --- Inizio logica per feed cumulativo ---
                    # 'current_trending_repos' contiene i repository attualmente di tendenza
                    final_repos_for_feed = list(current_trending_repos)
                    # Tiene traccia degli URL dei repo già inclusi per evitare duplicati
                    processed_repo_urls = {
                        repo["url"]
                        for repo in current_trending_repos
                        if "url" in repo
                    }

                    # Se il file JSON con i dati dei repository delle esecuzioni precedenti esiste,
                    # leggilo per aggiungere i repository storici.
                    if os.path.exists(trending_json_path):
                        try:
                            with open(
                                trending_json_path, "r", encoding="utf-8"
                            ) as f_json_old:
                                previous_repos_data = json.load(f_json_old)

                            # Filtra i vecchi repository e mantieni solo quelli
                            # che sono stati aggiornati negli ultimi `max_days` giorni.
                            filtered_previous_repos = []
                            repos_to_keep = []

                            if max_days > 0:
                                time_threshold = datetime.now(
                                    timezone.utc
                                ) - timedelta(days=max_days)
                                for repo in previous_repos_data:
                                    updated_at_str = repo.get("updated_at")
                                    if updated_at_str:
                                        try:
                                            # Converte la data in un oggetto datetime con timezone
                                            updated_at_dt = datetime.fromisoformat(
                                                updated_at_str.replace("Z", "+00:00")
                                            )
                                            if updated_at_dt > time_threshold:
                                                repos_to_keep.append(repo)
                                        except ValueError:
                                            # Ignora i repo con formati di data non validi
                                            continue
                                # Logica per aggiungere i repository storici filtrati
                                added_from_history_count = 0
                                for old_repo in repos_to_keep:
                                    if (
                                        "url" in old_repo
                                        and old_repo["url"]
                                        not in processed_repo_urls
                                    ):
                                        final_repos_for_feed.append(old_repo)
                                        processed_repo_urls.add(old_repo["url"])
                                        added_from_history_count += 1

                                # Messaggio di log per i repository scartati
                                discarded_count = len(previous_repos_data) - len(
                                    repos_to_keep
                                )
                                if discarded_count > 0:
                                    logging.info(
                                        f"Scartati {discarded_count} repository storici perché più vecchi di {max_days} giorni."
                                    )
                                if added_from_history_count > 0:
                                    logging.info(
                                        f"Aggiunti {added_from_history_count} repository storici da {trending_json_path}."
                                    )
                            else:
                                logging.info(
                                    "La conservazione dei dati storici è disabilitata (max_days=0)."
                                )
                        except json.JSONDecodeError:
                            logging.warning(
                                f"Impossibile decodificare il file JSON storico {trending_json_path}. Il feed non sarà arricchito."
                            )
                        except Exception as e:
                            logging.warning(
                                f"Errore durante la lettura o il filtraggio del file JSON storico {trending_json_path}: {e}"
                            )

                    # Opzionale: ordina la lista finale. Ad esempio, per numero di stelle (decrescente).
                    # Questo assicura un ordinamento consistente nel feed.
                    # Se non ordinato, i nuovi saranno prima, seguiti dai vecchi non duplicati.
                    if final_repos_for_feed:
                        final_repos_for_feed.sort(
                            key=lambda x: x.get("stars", 0), reverse=True
                        )
                    # --- Fine logica per feed cumulativo ---

                    # Salva la lista aggiornata e filtrata di repository nel file JSON.
                    # Questo file JSON funge da "database" per i prossimi aggiornamenti.
                    with open(trending_json_path, "w", encoding="utf-8") as file:
                        json.dump(
                            final_repos_for_feed, file, ensure_ascii=False, indent=2
                        )
                    logging.info(
                        f"Dati dei repository ({len(final_repos_for_feed)} totali) aggiornati e salvati in {trending_json_path}"
                    )

                    # Generate RSS feed
                    feed_title = f"GitHub Trending - {language} ({period.capitalize()})"

                    additional_description_note = ""
                    # Aggiungi una nota alla descrizione se il feed contiene dati storici
                    if len(final_repos_for_feed) > len(current_trending_repos):
                        additional_description_note = (
                            " (include repository da sessioni precedenti)"
                        )

                    feed_description = f"Repository più popolari su GitHub in {language} nel periodo {period.lower()}{additional_description_note}"
                    rss_feed = create_rss_feed(
                        final_repos_for_feed,  # Usa la lista finale (cumulativa)
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
                logging.exception(
                    f"Errore durante la generazione per {language} ({period}): {e}"
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
