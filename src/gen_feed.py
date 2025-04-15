# -*- coding: utf-8 -*-
# copyright Duccio Meconcelli 2025
# licenza MIT


import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime


def create_rss_feed(
    repos, title="GitHub Trending Repositories", description="Le repository più popolari su GitHub"
):
    """
    Crea un feed RSS dalle repository di GitHub

    Parameters:
    repos (list): Lista di repository organizzate
    title (str): Titolo del feed RSS
    description (str): Descrizione del feed RSS

    Returns:
    str: Feed RSS in formato XML
    """
    # Crea l'elemento root del feed RSS
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # Aggiungi i dettagli del feed
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = "https://github.com/trending"
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "it-IT"
    ET.SubElement(channel, "updated").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Aggiungi ogni repository come item nel feed
    for repo in repos:
        item = ET.SubElement(channel, "item")

        # Formatta il titolo con il nome e le stelle
        item_title = f"{repo['name']} ({repo['stars']} ⭐)"
        ET.SubElement(item, "title").text = item_title

        ET.SubElement(item, "link").text = repo["url"]

        # Formatta la descrizione HTML
        description = f"""
        <p><strong>Repository:</strong> {repo['name']}</p>
        <p><strong>Descrizione:</strong> {repo['description']}</p>
        <p><strong>Linguaggio:</strong> {repo['language']}</p>
        <p><strong>Stelle:</strong> {repo['stars']} ⭐</p>
        <p><strong>Fork:</strong> {repo['forks']}</p>
        <p><strong>Creata il:</strong> {repo['created_at']}</p>
        <p><a href="{repo['url']}">Visita repository</a></p>
        """
        ET.SubElement(item, "description").text = description

        # Genera un ID unico
        ET.SubElement(item, "guid", isPermaLink="false").text = repo["url"]

        # Aggiungi data di pubblicazione
        if repo.get("created_at"):
            try:
                pub_date = parser.parse(repo["created_at"]).strftime("%a, %d %b %Y %H:%M:%S +0000")
                ET.SubElement(item, "pubDate").text = pub_date
            except Exception:
                ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Converti l'albero XML in stringa
    xml_string = ET.tostring(rss, encoding="utf-8", method="xml")

    # Aggiungi l'intestazione XML e decodifica
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    return xml_declaration + xml_string.decode("utf-8")


def save_rss_feed(rss_feed, filename="github_trending.xml"):
    """
    Salva il feed RSS in un file

    Parameters:
    rss_feed (str): Contenuto del feed RSS
    filename (str): Nome del file di output

    Returns:
    bool: True se il salvataggio ha avuto successo, False altrimenti
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(rss_feed)
        return True
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")
        return False


def main():
    # Testa la generazione del feed RSS
    pass


if __name__ == "__main__":
    main()
