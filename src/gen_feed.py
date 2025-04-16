# -*- coding: utf-8 -*-
# copyright Duccio Meconcelli 2025
# licenza MIT


import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime, timezone
import email.utils  # Per formattare le date in RFC 822
import html  # Per fare l'escape di caratteri speciali nell'HTML


def create_rss_feed(
    repos,
    feed_url,
    title="GitHub Trending Repositories",
    description="The most popular repositories on GitHub",
):
    """
    Creates an RSS 2.0 feed from GitHub repositories

    Parameters:
    repos (list): List of organized repositories (should include 'telegraph_url')
    feed_url (str): The public URL where this feed will be hosted (used for channel link)
    title (str): Feed title
    description (str): Feed description

    Returns:
    str: RSS 2.0 feed in XML format
    """
    # Create root element <rss>
    rss = ET.Element("rss")
    rss.set("version", "2.0")
    # Aggiungi namespace atom per link self
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    # Create <channel> element
    channel = ET.SubElement(rss, "channel")

    # Add channel details
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = feed_url
    # Aggiungi link atom:self per una migliore scoperta del feed
    ET.SubElement(
        channel,
        "{http://www.w3.org/2005/Atom}link",
        href=feed_url,
        rel="self",
        type="application/rss+xml",
    )
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "it-it"  # Cambiato in italiano

    # Data dell'ultimo aggiornamento del feed (formato RFC 822)
    current_time_utc = datetime.now(timezone.utc)
    last_build_date = email.utils.format_datetime(current_time_utc)
    ET.SubElement(channel, "lastBuildDate").text = last_build_date
    # Opzionale: ET.SubElement(channel, "ttl").text = "60" # Time To Live in minuti

    # Add each repository as an <item>
    for repo in repos:
        item = ET.SubElement(channel, "item")

        # Format title with repo name, stars, and language emoji
        lang_emoji = "📝"  # Default emoji
        # Potresti mappare linguaggi comuni a emoji specifici qui se vuoi
        if repo.get("language") == "Python":
            lang_emoji = "🐍"
        elif repo.get("language") == "JavaScript":
            lang_emoji = "📜"
        elif repo.get("language") == "Go":
            lang_emoji = "🐹"
        elif repo.get("language") == "Rust":
            lang_emoji = "🦀"
        elif repo.get("language") == "TypeScript":
            lang_emoji = "🟦"
        elif repo.get("language") == "Java":
            lang_emoji = "☕"
        elif repo.get("language") == "C#":
            lang_emoji = "♯"
        elif repo.get("language") == "PHP":
            lang_emoji = "🐘"
        elif repo.get("language") == "C++":
            lang_emoji = "💻"
        # ... aggiungi altre mappature

        item_title = f"{lang_emoji} {repo['name']} ({repo['stars']} ⭐)"
        ET.SubElement(item, "title").text = item_title

        ET.SubElement(item, "link").text = repo["url"]
        ET.SubElement(item, "guid", isPermaLink="true").text = repo["url"]

        # Format description as HTML with more details and Telegraph link
        # Usiamo CDATA per includere HTML nella description
        # Usiamo html.escape per sicurezza sui dati forniti dall'utente (descrizione, nome repo, ecc.)
        repo_name_safe = html.escape(repo["name"])
        repo_desc_safe = html.escape(repo.get("description", "N/A"))
        repo_lang_safe = html.escape(repo.get("language", "N/A"))
        repo_license_safe = html.escape(repo.get("license", "N/A"))
        owner_name_safe = html.escape(repo.get("owner", {}).get("name", "N/A"))

        # Topics
        topics_html = ""
        if repo.get("topics"):
            topics_html = " ".join(
                f'<span style="background-color: #f0f0f0; padding: 2px 5px; border-radius: 3px; margin-right: 3px; font-size: 0.9em;">{html.escape(topic)}</span>'
                for topic in repo["topics"]
            )
            topics_html = f"<p><strong>🏷️ Topics:</strong> {topics_html}</p>"

        # Telegraph Link
        telegraph_link_html = ""
        if repo.get("telegraph_url"):
            telegraph_link_html = f'<p>📖 <a href="{html.escape(repo["telegraph_url"])}"><strong>Leggi il README su Telegraph</strong></a></p>'

        description_html = f"""
        <![CDATA[
        <p>👤 <strong>Owner:</strong> {owner_name_safe}</p>
        <p>📝 <strong>Repository:</strong> <a href="{html.escape(repo['url'])}">{repo_name_safe}</a></p>
        <p>📄 <strong>Descrizione:</strong> {repo_desc_safe}</p>
        <p>⭐ <strong>Stelle:</strong> {repo['stars']}</p>
        <p>🍴 <strong>Forks:</strong> {repo['forks']}</p>
        <p>💻 <strong>Linguaggio:</strong> {repo_lang_safe}</p>
        {topics_html}
        <p>📜 <strong>Licenza:</strong> {repo_license_safe}</p>
        <p>⏰ <strong>Creato il:</strong> {repo.get('created_at', 'N/A')}</p>
        <p>🔄 <strong>Ultimo Aggiornamento:</strong> {repo.get('updated_at', 'N/A')}</p>
        {telegraph_link_html}
        <hr>
        <p><a href="{html.escape(repo['url'])}">Visita il Repository su GitHub</a></p>
        ]]>
        """
        ET.SubElement(item, "description").text = description_html

        # Create RFC 822 formatted dates for pubDate (using updated_at for relevance)
        pub_date_source = repo.get("updated_at") or repo.get(
            "created_at"
        )  # Preferisci updated_at
        if pub_date_source:
            try:
                pub_date_dt = parser.parse(pub_date_source)
                if pub_date_dt.tzinfo is None:
                    pub_date_dt = pub_date_dt.replace(tzinfo=timezone.utc)
                else:
                    pub_date_dt = pub_date_dt.astimezone(timezone.utc)

                pub_date_str = email.utils.format_datetime(pub_date_dt)
                ET.SubElement(item, "pubDate").text = pub_date_str
            except Exception as e:
                print(
                    f"Warning: Failed to parse date '{pub_date_source}' for {repo['name']}: {e}"
                )
                ET.SubElement(item, "pubDate").text = last_build_date  # Fallback
        else:
            ET.SubElement(item, "pubDate").text = last_build_date  # Fallback

        # Aggiungi categoria/tag per il linguaggio
        if repo.get("language"):
            ET.SubElement(item, "category").text = repo["language"]
        # Aggiungi categorie/tag per i topics
        for topic in repo.get("topics", []):
            ET.SubElement(item, "category").text = topic

    # Convert XML tree to string
    # ET.indent(rss) # Aggiunge indentazione per leggibilità (richiede Python 3.9+)
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
    # Test feed generation (esempio con dati fittizi aggiornati)
    sample_repos = [
        {
            "name": "Test Repo 1",
            "stars": 123,
            "url": "https://github.com/user/test-repo-1",
            "description": "This is a test repository.",
            "language": "Python",
            "forks": 45,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2025-04-10T12:00:00Z",
            "telegraph_url": "https://telegra.ph/README-Test-Repo-1-04-16",  # Esempio URL Telegraph
            "topics": ["python", "test", "example"],
            "license": "MIT License",
            "owner": {"name": "testuser", "avatar_url": ""},
        },
        {
            "name": "Another Repo",
            "stars": 456,
            "url": "https://github.com/user/another-repo",
            "description": "Another great project. <script>alert('xss')</script>",  # Esempio con potenziale XSS
            "language": "JavaScript",
            "forks": 78,
            "created_at": "2025-03-20T14:30:00+01:00",
            "updated_at": "2025-04-15T09:15:00Z",
            "telegraph_url": None,  # Esempio senza URL Telegraph
            "topics": ["javascript", "web", "frontend"],
            "license": "Apache License 2.0",
            "owner": {"name": "anotheruser", "avatar_url": ""},
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
