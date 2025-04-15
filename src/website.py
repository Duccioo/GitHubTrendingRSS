from datetime import datetime


def generate_website():
    """
    Genera un sito web HTML per visualizzare i feed RSS delle repository di tendenza
    organizzate per linguaggio di programmazione e periodo di tempo.
    """
    # Definisci i linguaggi supportati
    languages = [
        "All Languages",
        "Unknown languages",
        "1C Enterprise",
        "2-Dimensional Array",
        "4D",
        "ABAP",
        "ABAP CDS",
        "ABNF",
        "ActionScript",
        "Ada",
        "Adblock Filter List",
        "Adobe Font Metrics",
        "Agda",
        "AGS Script",
        "AIDL",
        # Puoi aggiungere altri linguaggi a piacimento
    ]

    # Definisci i periodi di tempo
    periods = ["Daily", "Weekly", "Monthly"]

    # Crea la struttura base del sito HTML
    html = (
        """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending RSS</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        header {
            background-color: #1a92ff;
            color: white;
            text-align: center;
            padding: 1.5rem 0;
            margin-bottom: 2rem;
        }
        h1 {
            margin: 0;
        }
        .build-info {
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .language-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: 300px;
            margin-bottom: 30px;
            padding: 20px;
            text-align: center;
        }
        .language-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .feed-links {
            display: flex;
            justify-content: space-around;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .github-badge {
            display: inline-block;
            margin: 10px 0;
            padding: 5px 10px;
            background-color: #24292e;
            color: white;
            border-radius: 3px;
            font-size: 0.8rem;
        }
        .github-star {
            display: inline-block;
            margin: 10px 0;
            padding: 5px 10px;
            background-color: #fff;
            color: #24292e;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
            font-size: 0.8rem;
        }
        footer {
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            background-color: #f1f1f1;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>GitHub Trending RSS</h1>
        <div class="github-badge">Fetch and Generate RSS Feeds <span class="passing">passing</span></div>
        <div class="github-star">★ Star: 24</div>
        <div class="build-info">The latest build: """
        + datetime.now().strftime("%d %B, %Y")
        + """</div>
    </header>
    
    <div class="container">
"""
    )

    # Aggiungi una card per ogni linguaggio
    for language in languages:
        html += f"""
        <div class="language-card">
            <div class="language-title">{language}</div>
            <div class="feed-links">
"""
        # Aggiungi i link per ogni periodo di tempo
        for period in periods:
            language_param = language.replace(" ", "%20")
            language_filename = language.replace(" ", "_").lower()
            period_lower = period.lower()
            html += f"""
                <a href="feeds/{language_filename}_{period_lower}.xml">{period}</a>
"""

        html += """
            </div>
        </div>
"""

    # Chiudi l'HTML
    html += """
    </div>
    
    <footer>
        <p>Generato automaticamente con Python | <a href="https://github.com/duccioo/GitHubTrendingRSS">Codice sorgente</a></p>
    </footer>
</body>
</html>
"""

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
