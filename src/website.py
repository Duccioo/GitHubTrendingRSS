import os
import json
import html
from datetime import datetime
from template import get_html_template

# --- Constants ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TARGET_BEST_FEED_FILE = os.path.join(DATA_DIR, "all_languages_monthly.xml")
NUM_POPULAR_EXAMPLES = 9
# Define supported languages
ALL_LANGUAGES_LIST = [
    "All Languages",
    "Unknown languages",
    "Python",
    "JavaScript",
    "Go",
    "Rust",
    "TypeScript",
    "Java",
    "C#",
    "PHP",
    "C++",
    "Swift",
    "Kotlin",
    "Ruby",
    "HTML",
    "CSS",
]
ALL_LANGUAGES_LIST.sort()  # Ensure consistent order initially

# Separate main languages
MAIN_LANGUAGES = ["All Languages"]
# Derive other languages
OTHER_LANGUAGES = [lang for lang in ALL_LANGUAGES_LIST if lang not in MAIN_LANGUAGES]
# Ensure other languages are also sorted
OTHER_LANGUAGES.sort()


# --- Helper Functions ---


def generate_popular_repo_cards(repos_data):
    """Generates HTML for popular repository cards, including Star History charts."""
    cards_html = ""

    if not repos_data:
        return "<p>No data available for popular repositories.</p>"

    # Emojis for stats
    star_emoji = "⭐"
    fork_emoji = "🍴"
    lang_emoji = "💻"

    for repo in repos_data[:NUM_POPULAR_EXAMPLES]:

        print(f"Processing popular repo: {repo.get('name')}")

        repo_full_name = repo.get("name")  # Get the full name (owner/repo)
        if not repo_full_name or "/" not in repo_full_name:
            print(f"Skipping popular repo card due to invalid name: {repo_full_name}")
            continue  # Skip if name is invalid for Star History

        # Escape data for HTML safety
        repo_name_safe = html.escape(repo_full_name)
        repo_url = html.escape(repo.get("url", "#"))
        repo_desc_raw = repo.get("description", "No description available.")
        if not repo_desc_raw:
            repo_desc_raw = "No description available."
        if len(repo_desc_raw) > 150:
            repo_desc_raw = repo_desc_raw[:147] + "..."
        repo_desc = html.escape(repo_desc_raw)  # Escape description

        repo_stars = repo.get("stars", 0)
        repo_forks = repo.get("forks", 0)
        repo_lang = repo.get("language", "N/A")  # Escape language
        if not repo_lang:
            repo_lang = "N/A"

        # --- Star History Integration ---
        # URL-encode the repository name for the API query parameter
        # No need to double-encode if the source name is already owner/repo
        encoded_repo_name = repo_full_name

        star_history_svg_url = f"https://api.star-history.com/svg?repos={encoded_repo_name}&type=Date&theme=dark"

        star_history_link_url = f"https://star-history.com/#{encoded_repo_name}&Date"  # Link to interactive chart

        star_history_html = f"""
            <div class="star-history-chart">
                <a href="{html.escape(star_history_link_url)}" target="_blank" rel="noopener noreferrer" title="View Star History for {repo_name_safe}">
                    
                    <img src="{html.escape(star_history_svg_url)}" alt="Star History Chart for {repo_name_safe}" loading="lazy">
                </a>
            </div>
        """

        # --- End Star History Integration ---

        cards_html += f"""
            <div class="popular-repo-card">
                <div class="repo-title"><a href="{repo_url}" target="_blank" rel="noopener noreferrer">{repo_name_safe}</a></div>
                <div class="repo-description">{repo_desc}</div>
                {star_history_html}
                <div class="repo-stats">
                    <span class="stars" title="Stars"><span class="emoji">{star_emoji}</span> {repo_stars}</span>
                    <span title="Forks"><span class="emoji">{fork_emoji}</span> {repo_forks}</span>
                    <span title="Language"><span class="emoji">{lang_emoji}</span> {repo_lang}</span>
                </div>
            </div>
        """

    return cards_html


def generate_website():
    """
    Generates an HTML website with categorized feed links.
    """
    periods = ["Daily", "Weekly", "Monthly"]
    rss_emoji = "📰"
    build_date = datetime.now().strftime("%d %B %Y, %H:%M:%S %Z")
    html_template = get_html_template(build_date)

    # --- Generate "New Repositories" Section ---
    new_repos_main_links_html = ""
    for language in MAIN_LANGUAGES:
        new_repos_main_links_html += f'<div class="main-language-group">'
        new_repos_main_links_html += f"<h3>{html.escape(language)}</h3>"
        new_repos_main_links_html += '<div class="feed-links">'
        for period in periods:
            lang_fn = language.replace(" ", "_").lower()
            feed_filename = f"{lang_fn}_{period.lower()}_new.xml"
            feed_path = f"feeds/{feed_filename}"
            new_repos_main_links_html += f'<a href="{html.escape(feed_path)}" class="feed-link"><span class="emoji">{rss_emoji}</span>{html.escape(period)}</a>'
        new_repos_main_links_html += "</div></div>"

    new_repos_other_cards_html = ""
    for language in OTHER_LANGUAGES:
        new_repos_other_cards_html += f'<div class="language-card"><div class="language-title">{html.escape(language)}</div><div class="feed-links">'
        for period in periods:
            lang_fn = language.replace(" ", "_").lower()
            feed_filename = f"{lang_fn}_{period.lower()}_new.xml"
            feed_path = f"feeds/{feed_filename}"
            new_repos_other_cards_html += f'<a href="{html.escape(feed_path)}" class="feed-link"><span class="emoji">{rss_emoji}</span>{html.escape(period)}</a>'
        new_repos_other_cards_html += "</div></div>"

    # --- Generate "Recently Updated" Section ---
    updated_repos_links_html = '<div class="main-language-group">'
    updated_repos_links_html += f"<h3>All Languages</h3>"
    updated_repos_links_html += '<div class="feed-links">'
    for period in periods:
        feed_filename = f"all_languages_{period.lower()}_last_update.xml"
        feed_path = f"feeds/{feed_filename}"
        updated_repos_links_html += f'<a href="{html.escape(feed_path)}" class="feed-link"><span class="emoji">{rss_emoji}</span>{html.escape(period)}</a>'
    updated_repos_links_html += "</div></div>"

    # --- Generate Popular Repo Cards ---
    target_feed_file = os.path.join(DATA_DIR, "all_languages_weekly_new.json")
    popular_cards_html = ""
    if os.path.exists(target_feed_file):
        try:
            with open(target_feed_file, "r", encoding="utf-8") as file:
                popular_repos = json.load(file)
            popular_repos.sort(key=lambda x: x.get("stars", 0), reverse=True)
            popular_cards_html = generate_popular_repo_cards(popular_repos)
        except Exception as e:
            print(f"Error processing {target_feed_file}: {e}")
            popular_cards_html = "<p>Error loading popular repositories.</p>"
    else:
        popular_cards_html = f"<p>Data feed not found.</p>"

    # --- Insert sections into the template ---
    html_output = html_template.replace(
        "<!-- Main language links will be inserted here -->", new_repos_main_links_html
    )
    html_output = html_output.replace(
        "<!-- Other language cards will be inserted here -->",
        new_repos_other_cards_html,
    )
    html_output = html_output.replace(
        "<!-- Recently updated links will be inserted here -->",
        updated_repos_links_html,
    )
    html_output = html_output.replace(
        "<!-- Popular repo examples will be inserted here -->", popular_cards_html
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
    # Define output directory (e.g., project root)
    output_directory = os.path.join(os.path.dirname(__file__), "..")

    # --- Generate the website HTML content ---
    print("Generating website...")
    html_content = generate_website()

    # Save the website to index.html in the output directory
    if save_website(html_content, output_dir=output_directory, filename="index.html"):
        print(
            f"Website generated and saved as {os.path.join(output_directory, 'index.html')}"
        )
    else:
        print("Error saving the website.")


if __name__ == "__main__":
    main()
