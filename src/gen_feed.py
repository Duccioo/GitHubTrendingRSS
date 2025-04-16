# -*- coding: utf-8 -*-
# copyright Duccio Meconcelli 2025
# licenza MIT


import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime


def create_rss_feed(
    repos, title="GitHub Trending Repositories", description="The most popular repositories on GitHub"
):
    """
    Creates an Atom feed from GitHub repositories

    Parameters:
    repos (list): List of organized repositories
    title (str): Feed title
    description (str): Feed description

    Returns:
    str: Atom feed in XML format
    """
    # Create namespace for Atom
    namespace = "http://www.w3.org/2005/Atom"
    media_namespace = "http://search.yahoo.com/mrss/"
    ET.register_namespace("", namespace)
    ET.register_namespace("media", media_namespace)

    # Create root element
    feed = ET.Element("{%s}feed" % namespace)
    feed.set("xml:lang", "en-us")

    # Add feed details
    ET.SubElement(feed, "{%s}title" % namespace).text = title

    link_alternate = ET.SubElement(feed, "{%s}link" % namespace)
    link_alternate.set("href", "https://github.com/trending")
    link_alternate.set("rel", "alternate")

    link_self = ET.SubElement(feed, "{%s}link" % namespace)
    link_self.set("href", "https://github.com/trending")
    link_self.set("rel", "self")

    ET.SubElement(feed, "{%s}id" % namespace).text = "https://github.com/trending"

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    ET.SubElement(feed, "{%s}updated" % namespace).text = current_time

    author = ET.SubElement(feed, "{%s}author" % namespace)
    ET.SubElement(author, "{%s}name" % namespace).text = "GitHub Trending RSS"

    ET.SubElement(feed, "{%s}subtitle" % namespace).text = description

    # Add each repository as an entry
    for repo in repos:
        entry = ET.SubElement(feed, "{%s}entry" % namespace)

        # Format title with repo name and stars
        item_title = f"{repo['name']} ({repo['stars']} ⭐)"
        ET.SubElement(entry, "{%s}title" % namespace).text = item_title

        link = ET.SubElement(entry, "{%s}link" % namespace)
        link.set("href", repo["url"])
        link.set("rel", "alternate")

        # Create ISO formatted dates
        if repo.get("created_at"):
            try:
                pub_date = parser.parse(repo["created_at"]).strftime("%Y-%m-%dT%H:%M:%S+00:00")
                ET.SubElement(entry, "{%s}published" % namespace).text = pub_date
                ET.SubElement(entry, "{%s}updated" % namespace).text = pub_date
            except Exception:
                ET.SubElement(entry, "{%s}published" % namespace).text = current_time
                ET.SubElement(entry, "{%s}updated" % namespace).text = current_time
        else:
            ET.SubElement(entry, "{%s}published" % namespace).text = current_time
            ET.SubElement(entry, "{%s}updated" % namespace).text = current_time

        ET.SubElement(entry, "{%s}id" % namespace).text = repo["url"]

        # Format description as HTML summary
        description_html = f"""
        <p><strong>Repository:</strong> {repo['name']}</p>
        <p><strong>Description:</strong> {repo['description']}</p>
        <p><strong>Language:</strong> {repo['language']}</p>
        <p><strong>Stars:</strong> {repo['stars']} ⭐</p>
        <p><strong>Forks:</strong> {repo['forks']}</p>
        <p><strong>Created on:</strong> {repo['created_at']}</p>
        <p><a href="{repo['url']}">Visit repository</a></p>
        """
        summary = ET.SubElement(entry, "{%s}summary" % namespace)
        summary.set("type", "html")
        summary.text = description_html

    # Convert XML tree to string
    xml_string = ET.tostring(feed, encoding="utf-8", method="xml")

    # Add XML declaration and decode
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    return xml_declaration + xml_string.decode("utf-8")


def save_rss_feed(rss_feed, filename="github_trending.xml"):
    """
    Saves the Atom feed to a file

    Parameters:
    rss_feed (str): Atom feed content
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
    # Test feed generation
    pass


if __name__ == "__main__":
    main()
