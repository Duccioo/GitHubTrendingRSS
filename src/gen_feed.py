# -*- coding: utf-8 -*-
# copyright Duccio Meconcelli 2025
# licenza MIT


import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime, timezone
import email.utils  # Per formattare le date in RFC 822


def create_rss_feed(
    repos,
    feed_url,
    title="GitHub Trending Repositories",
    description="The most popular repositories on GitHub",
):
    """
    Creates an RSS 2.0 feed from GitHub repositories

    Parameters:
    repos (list): List of organized repositories
    feed_url (str): The public URL where this feed will be hosted (used for channel link)
    title (str): Feed title
    description (str): Feed description

    Returns:
    str: RSS 2.0 feed in XML format
    """
    # Create root element <rss>
    rss = ET.Element("rss")
    rss.set("version", "2.0")
    # Aggiungi namespace per content:encoded se necessario per HTML completo
    # rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")

    # Create <channel> element
    channel = ET.SubElement(rss, "channel")

    # Add channel details
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = feed_url  # Link al sito o alla pagina principale del feed
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "en-us"  # Lingua del feed

    # Data dell'ultimo aggiornamento del feed (formato RFC 822)
    current_time_utc = datetime.now(timezone.utc)
    last_build_date = email.utils.format_datetime(current_time_utc)
    ET.SubElement(channel, "lastBuildDate").text = last_build_date
    # Opzionale: ET.SubElement(channel, "pubDate").text = last_build_date
    # Opzionale: ET.SubElement(channel, "ttl").text = "60" # Time To Live in minuti

    # Add each repository as an <item>
    for repo in repos:
        item = ET.SubElement(channel, "item")

        # Format title with repo name and stars
        item_title = f"{repo['name']} ({repo['stars']} ⭐)"
        ET.SubElement(item, "title").text = item_title

        ET.SubElement(item, "link").text = repo["url"]
        ET.SubElement(item, "guid", isPermaLink="true").text = repo["url"]  # GUID univoco, spesso l'URL

        # Format description as HTML
        # Usiamo CDATA per includere HTML nella description
        description_html = f"""
        <![CDATA[
        <p><strong>Repository:</strong> {repo['name']}</p>
        <p><strong>Description:</strong> {repo['description']}</p>
        <p><strong>Language:</strong> {repo['language']}</p>
        <p><strong>Stars:</strong> {repo['stars']} ⭐</p>
        <p><strong>Forks:</strong> {repo['forks']}</p>
        <p><strong>Created on:</strong> {repo['created_at']}</p>
        <p><a href="{repo['url']}">Visit repository</a></p>
        ]]>
        """
        ET.SubElement(item, "description").text = description_html
        # Alternativa per HTML completo (richiede namespace content):
        # content_encoded = ET.SubElement(item, "{http://purl.org/rss/1.0/modules/content/}encoded")
        # content_encoded.text = description_html # Senza CDATA qui

        # Create RFC 822 formatted dates for pubDate
        if repo.get("created_at"):
            try:
                # Assicurati che la data sia consapevole del fuso orario (UTC)
                pub_date_dt = parser.parse(repo["created_at"])
                if pub_date_dt.tzinfo is None:
                    # Se non c'è fuso orario, assumi UTC (o il fuso orario corretto se noto)
                    pub_date_dt = pub_date_dt.replace(tzinfo=timezone.utc)
                else:
                    # Converti a UTC se ha un fuso orario diverso
                    pub_date_dt = pub_date_dt.astimezone(timezone.utc)

                pub_date_str = email.utils.format_datetime(pub_date_dt)
                ET.SubElement(item, "pubDate").text = pub_date_str
            except Exception:
                # Fallback alla data corrente se il parsing fallisce
                ET.SubElement(item, "pubDate").text = last_build_date
        else:
            # Fallback alla data corrente se 'created_at' manca
            ET.SubElement(item, "pubDate").text = last_build_date

    # Convert XML tree to string
    xml_string = ET.tostring(rss, encoding="utf-8", method="xml")

    # Add XML declaration and decode
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    return xml_declaration + xml_string.decode("utf-8")


def save_rss_feed(rss_feed, filename="github_trending.xml"):
    """
    Saves the RSS feed to a file

    Parameters:
    rss_feed (str): RSS feed content
    filename (str): Output file name

    Returns:
    bool: True if the save was successful, False otherwise
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(rss_feed)
        return True
    except Exception as e:
        print(f"Error while saving the file: {e}")
        return False


def main():
    # Test feed generation (esempio con dati fittizi)
    sample_repos = [
        {
            "name": "Test Repo 1",
            "stars": 123,
            "url": "https://github.com/user/test-repo-1",
            "description": "This is a test repository.",
            "language": "Python",
            "forks": 45,
            "created_at": "2024-01-15T10:00:00Z",  # Formato ISO 8601
        },
        {
            "name": "Another Repo",
            "stars": 456,
            "url": "https://github.com/user/another-repo",
            "description": "Another great project.",
            "language": "JavaScript",
            "forks": 78,
            "created_at": "2025-03-20T14:30:00+01:00",  # Formato ISO 8601 con fuso orario
        },
    ]
    feed_content = create_rss_feed(sample_repos, "https://example.com/rss.xml")
    print("Generated RSS Feed:")
    # print(feed_content) # Stampa il feed generato (può essere lungo)
    if save_rss_feed(feed_content, "test_rss_feed.xml"):
        print("Test RSS feed saved to test_rss_feed.xml")
    else:
        print("Failed to save test RSS feed.")


if __name__ == "__main__":
    main()
