# Importa le librerie necessarie
import os
import time
from datetime import datetime
import website

# ----
from repo_scraper import get_trending_repositories, extract_repo_data
from gen_feed import create_rss_feed


def generate_all_feeds():
    """
    Genera feed RSS per tutti i linguaggi e periodi di tempo definiti
    e li salva nella cartella 'feeds'.
    """
    # Definisci i linguaggi supportati
    languages = [
        "All Languages",
        "Unknown languages",
        # Puoi aggiungere altri linguaggi a piacimento
    ]

    # Definisci i periodi di tempo
    periods = ["daily", "weekly", "monthly"]

    # Crea la cartella feeds se non esiste
    if not os.path.exists("feeds"):
        os.makedirs("feeds")
        print("Creata cartella 'feeds'")

    count = 0
    errors = 0

    # Genera feed per ogni combinazione di linguaggio e periodo
    for language in languages:
        for period in periods:
            try:
                print(f"Generazione feed per {language} ({period})...")

                # Usa None per 'All Languages' e converti appropriatamente per 'Unknown languages'
                lang_param = None if language == "All Languages" else language
                if language == "Unknown languages":
                    lang_param = "Unknown"

                # Recupera repository
                repos = get_trending_repositories(language=lang_param, since=period, limit=30)

                if repos:
                    # Organizza i dati
                    organized_repos = extract_repo_data(repos)

                    # Genera feed RSS
                    feed_title = f"GitHub Trending - {language} ({period})"
                    feed_description = (
                        f"Le repository più popolari in {language} nell'ultimo periodo {period}"
                    )
                    rss_feed = create_rss_feed(
                        organized_repos, title=feed_title, description=feed_description
                    )

                    # Salva feed RSS
                    filename = f"feeds/{language.replace(' ', '_').lower()}_{period}.xml"
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(rss_feed)

                    count += 1
                    print(f"Feed salvato: {filename}")

                    # Aggiungi piccola pausa per evitare troppe richieste API
                    time.sleep(1)
                else:
                    print(f"Nessuna repository trovata per {language} ({period})")
                    errors += 1

            except Exception as e:
                print(f"Errore per {language} ({period}): {str(e)}")
                errors += 1

    print(f"\nCompletato! Feed generati: {count}, errori: {errors}")
    return count, errors


def main():
    # Assicurati che esista la directory dei feeds
    os.makedirs("feeds", exist_ok=True)

    # Qui potresti chiamare altre funzioni per generare i feed RSS
    generate_all_feeds()

    # Genera e salva il sito web
    html_content = website.generate_website()
    if website.save_website(html_content):
        print(f"Sito web generato e salvato come index.html")
    else:
        print("Errore durante il salvataggio del sito web")


if __name__ == "__main__":
    print(f"Inizio esecuzione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    print(f"Fine esecuzione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
