from datetime import datetime
from template import get_html_template


def generate_website():
    """
    Genera un sito web HTML per visualizzare i feed RSS delle repository di tendenza
    organizzate per linguaggio di programmazione e periodo di tempo.
    """
    # Definisci i linguaggi supportati
    languages = [
        "All Languages",
        "Unknown languages",
        # Puoi aggiungere altri linguaggi a piacimento
    ]

    # Definisci i periodi di tempo
    periods = ["Daily", "Weekly", "Monthly"]

    # Ottieni la data di build attuale
    build_date = datetime.now().strftime("%d %B, %Y")

    # Ottieni il template HTML base
    html = get_html_template(build_date)

    # Prepara le card dei linguaggi per inserirle nel template
    language_cards = ""

    for language in languages:
        language_cards += f"""
            <div class="language-card">
                <div class="language-title">{language}</div>
                <div class="feed-links">
        """

        # Aggiungi i link per ogni periodo di tempo
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

    # Inserisci le card dei linguaggi nel template
    html = html.replace("<!-- Qui verranno inserite le card dei linguaggi -->", language_cards)

    return html


def save_website(html_content, filename="index.html"):
    """
    Salva il contenuto HTML in un file

    Parameters:
    html_content (str): Contenuto HTML del sito web
    filename (str): Nome del file di output

    Returns:
    bool: True se il salvataggio ha avuto successo, False altrimenti
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        return True
    except Exception as e:
        print(f"Errore durante il salvataggio del file HTML: {e}")
        return False


def main():
    # Genera il sito web
    html_content = generate_website()

    # Salva il sito web in un file
    if save_website(html_content):
        print("Sito web generato e salvato come index.html")
    else:
        print("Errore durante il salvataggio del sito web")


if __name__ == "__main__":
    main()
