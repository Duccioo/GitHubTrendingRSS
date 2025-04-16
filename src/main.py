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
    Generates Atom feeds for all languages and time periods
    and saves them in the 'feeds' folder.
    """

    # Definisci l'URL base per i tuoi feed
    base_feed_url = "https://duccioo.github.io/GitHubTrendingRSS_duccioo/"  # Modifica se necessario

    # Define supported languages
    languages = [
        "All Languages",
        "Unknown languages",
        # You can add more languages as needed
    ]

    # Define time periods
    periods = ["daily", "weekly", "monthly"]

    # Create feeds folder if it doesn't exist
    if not os.path.exists("feeds"):
        os.makedirs("feeds")
        print("Created 'feeds' folder")

    count = 0
    errors = 0

    # Generate feed for each language and period combination
    for language in languages:
        for period in periods:
            try:
                print(f"Generating feed for {language} ({period})...")

                # Use None for 'All Languages' and convert appropriately for 'Unknown languages'
                lang_param = None if language == "All Languages" else language
                if language == "Unknown languages":
                    lang_param = "Unknown"

                # Get repositories
                repos = get_trending_repositories(language=lang_param, since=period, limit=30)

                if repos:
                    # Organize data
                    organized_repos = extract_repo_data(repos)

                    # Costruisci l'URL e il nome del file specifici
                    filename = f"feeds/{language.replace(' ', '_').lower()}_{period}.xml"
                    feed_url = f"{base_feed_url}{filename}"

                    # Generate Atom feed
                    feed_title = f"GitHub Trending - {language} ({period})"
                    feed_description = f"The most popular repositories in {language} for the {period} period"
                    atom_feed = create_rss_feed(
                        organized_repos, feed_url=feed_url, title=feed_title, description=feed_description
                    )

                    # Save Atom feed

                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(atom_feed)

                    count += 1
                    print(f"Feed saved: {filename}")

                    # Add a small pause to avoid too many API requests
                    time.sleep(1)
                else:
                    print(f"No repositories found for {language} ({period})")
                    errors += 1

            except Exception as e:
                print(f"Error for {language} ({period}): {str(e)}")
                errors += 1

    print(f"\nCompleted! Feeds generated: {count}, errors: {errors}")
    return count, errors


def main():
    # Make sure the feeds directory exists
    os.makedirs("feeds", exist_ok=True)

    # Generate all feeds
    generate_all_feeds()

    # Generate and save the website
    html_content = website.generate_website()
    if website.save_website(html_content, "index.html"):
        print(f"Website generated and saved as index.html")
    else:
        print("Error while saving the website")


if __name__ == "__main__":
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    print(f"Execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
