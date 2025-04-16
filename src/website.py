import os
import json
import html
from datetime import datetime
from template import get_html_template

# --- Constants ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TRENDING_JSON_FILE = os.path.join(DATA_DIR, "trending_repos.json")
NUM_POPULAR_EXAMPLES = 4

# --- Helper Functions ---


def generate_popular_repo_cards(repos_data):
    """Generates HTML for popular repository cards."""
    cards_html = ""
    if not repos_data:
        return "<p>No data available for popular repositories.</p>"

    star_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M12,17.27L18.18,21L17,14.64L22,9.73L14.81,8.63L12,2L9.19,8.63L2,9.73L7,14.64L5.82,21L12,17.27Z"/></svg>'
    fork_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#bbbbbb" width="1em" height="1em"><path d="M8,4 C9.1,4 10,4.9 10,6 L10,8 C10,9.1 9.1,10 8,10 L6,10 C4.9,10 4,9.1 4,8 L4,6 C4,4.9 4.9,4 6,4 L8,4 M8,2 L6,2 C3.79,2 2,3.79 2,6 L2,8 C2,10.21 3.79,12 6,12 L8,12 C10.21,12 12,10.21 12,8 L12,6 C12,3.79 10.21,2 8,2 M18,14 C19.1,14 20,14.9 20,16 L20,18 C20,19.1 19.1,20 18,20 L16,20 C14.9,20 14,19.1 14,18 L14,16 C14,14.9 14.9,14 16,14 L18,14 M18,12 L16,12 C13.79,12 12,13.79 12,16 L12,18 C12,20.21 13.79,22 16,22 L18,22 C20.21,22 22,20.21 22,18 L22,16 C22,13.79 20.21,12 18,12 M10,7 L10,13.5 C10,14.04 10.22,14.55 10.59,14.91 L14,18.3 L14,7 C14,6.45 13.55,6 13,6 L11,6 C10.45,6 10,6.45 10,7 Z"/></svg>'
    lang_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#bbbbbb" width="1em" height="1em"><path d="M9.4,16.6L4.8,12L9.4,7.4L8,6L2,12L8,18L9.4,16.6M14.6,16.6L19.2,12L14.6,7.4L16,6L22,12L16,18L14.6,16.6Z"/></svg>'

    for repo in repos_data[:NUM_POPULAR_EXAMPLES]:
        repo_name = html.escape(repo.get("name", "N/A"))
        repo_url = html.escape(repo.get("url", "#"))
        repo_desc = html.escape(repo.get("description", "No description available."))
        if len(repo_desc) > 150:
            repo_desc = repo_desc[:147] + "..."

        repo_stars = repo.get("stars", 0)
        repo_forks = repo.get("forks", 0)
        repo_lang = html.escape(repo.get("language", "N/A"))

        cards_html += f"""
            <div class="popular-repo-card">
                <div class="repo-title"><a href="{repo_url}" target="_blank" rel="noopener noreferrer">{repo_name}</a></div>
                <div class="repo-description">{repo_desc}</div>
                <div class="repo-stats">
                    <span class="stars" title="Stars">{star_svg} {repo_stars}</span>
                    <span title="Forks">{fork_svg} {repo_forks}</span>
                    <span title="Language">{lang_svg} {repo_lang}</span>
                </div>
            </div>
        """
    return cards_html


def generate_website(popular_repos_data):
    """
    Generates an HTML website to display the RSS feeds and popular repos.

    Parameters:
    popular_repos_data (list): List of dictionaries for popular repositories.
    """
    languages = [
        "All Languages",
        "Unknown languages",
        "Python",
        "JavaScript",
        "Go",
        "Rust",
        "TypeScript",
        "PHP",
        "C++",
        "Swift",
        "HTML",
        "CSS",
    ]
    languages.sort()

    periods = ["Daily", "Weekly", "Monthly"]

    build_date = datetime.now().strftime("%d %B %Y, %H:%M:%S %Z")

    html_template = get_html_template(build_date)

    language_cards = ""
    rss_svg_icon = '<span class="rss-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M6,19h4C10,14.37,5.63,10,1,10v4C3.59,14,6,16.41,6,19z M3.9,17.1C3.9,16.36,3.26,15.9,2.5,15.9s-1.4,0.46-1.4,1.2s0.63,1.2,1.4,1.2S3.9,17.85,3.9,17.1z M17,19h4v-4c-4.63,0-9,4.37-9,9h4C16,21.41,14.93,19,17,19z M12,10v4c3.59,0,6.5,2.91,6.5,6.5h4C22.5,14.09,17.91,10,12,10z" /></svg></span>'

    for language in languages:
        language_cards += f"""
            <div class="language-card">
                <div class="language-title">{html.escape(language)}</div>
                <div class="feed-links">
        """
        for period in periods:
            lang_filename_part = (
                language.replace(" ", "_")
                .replace("#", "sharp")
                .replace("+", "plus")
                .lower()
            )
            period_lower = period.lower()
            feed_filename = f"{lang_filename_part}_{period_lower}.xml"
            feed_path = f"feeds/{feed_filename}"

            language_cards += f"""
                    <a href="{feed_path}" class="feed-link">
                        {rss_svg_icon}{html.escape(period)}
                    </a>
            """
        language_cards += """
                </div>
            </div>
        """

    popular_cards_html = generate_popular_repo_cards(popular_repos_data)

    html_output = html_template.replace(
        "<!-- Qui verranno inserite le card dei linguaggi -->", language_cards
    )
    html_output = html_output.replace(
        "<!-- Qui verranno inseriti gli esempi di repo popolari -->", popular_cards_html
    )

    return html_output


def save_website(html_content, output_dir=".", filename="index.html"):
    """
    Saves the HTML content to a file in the specified directory.
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory {output_dir}: {e}")
            return False

    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html_content)
        return True
    except Exception as e:
        print(f"Error saving HTML file {filepath}: {e}")
        return False


def main():
    output_directory = os.path.join(os.path.dirname(__file__), "..")

    popular_repos = []
    try:
        with open(TRENDING_JSON_FILE, "r", encoding="utf-8") as f:
            all_repos = json.load(f)
            popular_repos = sorted(
                all_repos, key=lambda x: x.get("stars", 0), reverse=True
            )
        print(f"Loaded {len(popular_repos)} repositories from {TRENDING_JSON_FILE}.")
    except FileNotFoundError:
        print(
            f"Warning: File {TRENDING_JSON_FILE} not found. Popular repositories section will be empty."
        )
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from {TRENDING_JSON_FILE}.")
    except Exception as e:
        print(f"Unexpected error loading {TRENDING_JSON_FILE}: {e}")

    html_content = generate_website(popular_repos)

    if save_website(html_content, output_dir=output_directory, filename="index.html"):
        print(
            f"Website generated and saved as {os.path.join(output_directory, 'index.html')}"
        )
    else:
        print("Error saving the website.")


if __name__ == "__main__":
    main()
