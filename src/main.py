# Importa le librerie necessarie
import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
from dateutil import parser
import time


# ----
from website import generate_website, save_website
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


# Esegui la generazione di tutti i feed
feeds_count, feeds_errors = generate_all_feeds()


def main_complete():
    """
    Processo completo per generare tutti i feed RSS e il sito web
    """
    print("Avvio generazione del sistema completo di feed RSS GitHub trending...\n")

    # 1. Genera tutti i feed RSS
    print("\n=== GENERAZIONE FEED RSS ===\n")
    feeds_count, feeds_errors = generate_all_feeds()

    # 2. Genera il sito web
    print("\n=== GENERAZIONE SITO WEB ===\n")
    html_content = generate_website()
    success = save_website(html_content, filename="index.html")

    if success:
        print(f"Il sito web è stato salvato con successo in 'index.html'")
    else:
        print(f"Si è verificato un errore durante il salvataggio del sito web")

    print("\n=== RIEPILOGO ===\n")
    print(f"Feed RSS generati: {feeds_count}")
    print(f"Feed RSS con errori: {feeds_errors}")
    print(f"Sito web generato: {'Sì' if success else 'No'}")
    print("\nPuoi aprire index.html nel tuo browser per visualizzare e accedere ai feed RSS")


# Eseguiamo tutto il processo completo se lo script viene eseguito direttamente
if __name__ == "__main__":
    main_complete()
