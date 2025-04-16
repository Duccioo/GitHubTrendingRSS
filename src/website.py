from datetime import datetime
from template import get_html_template


def generate_website():
    """
    Generates an HTML website to display the RSS feeds of trending repositories
    organized by programming language and time period.
    """
    # Define supported languages
    languages = [
        "All Languages",
        "Unknown languages",
        # You can add more languages as needed
    ]

    # Define time periods
    periods = ["Daily", "Weekly", "Monthly"]

    # Get current build date
    build_date = datetime.now().strftime("%d %B, %Y")

    # Get the base HTML template
    html = get_html_template(build_date)

    # Prepare language cards to insert in the template
    language_cards = ""

    for language in languages:
        language_cards += f"""
            <div class="language-card">
                <div class="language-title">{language}</div>
                <div class="feed-links">
        """

        # Add links for each time period
        for period in periods:
            language_filename = language.replace(" ", "_").lower()
            period_lower = period.lower()
            language_cards += f"""
                    <a href="feeds/{language_filename}_{period_lower}.xml" class="feed-link">
                        <span class="rss-icon"></span>{period}
                    </a>
            """

        language_cards += """
                </div>
            </div>
        """

    # Insert language cards into the template
    html = html.replace("<!-- Qui verranno inserite le card dei linguaggi -->", language_cards)

    return html


def save_website(html_content, filename="index.html"):
    """
    Saves the HTML content to a file

    Parameters:
    html_content (str): HTML content of the website
    filename (str): Output file name

    Returns:
    bool: True if the save was successful, False otherwise
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        return True
    except Exception as e:
        print(f"Error while saving the HTML file: {e}")
        return False


def main():
    # Generate the website
    html_content = generate_website()

    # Save the website to a file
    if save_website(html_content):
        print("Website generated and saved as index.html")
    else:
        print("Error while saving the website")


if __name__ == "__main__":
    main()
