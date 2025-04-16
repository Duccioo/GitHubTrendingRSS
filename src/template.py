"""
Questo modulo contiene il template HTML per il sito web GitHubTrendingRSS.
"""


def get_html_template(build_date):
    """
    Restituisce il template HTML con la data di build specificata.

    Parameters:
    build_date (str): Data di generazione del sito

    Returns:
    str: Template HTML
    """
    # Icona Fulmine SVG (giallo)
    lightning_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M11 21H7V14H2V11.5L3.5 5.75L4 5H17L16.5 7H11V12H15L11 21Z"/></svg>'
    # Icona RSS SVG (giallo)
    rss_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M6,19h4C10,14.37,5.63,10,1,10v4C3.59,14,6,16.41,6,19z M3.9,17.1C3.9,16.36,3.26,15.9,2.5,15.9s-1.4,0.46-1.4,1.2s0.63,1.2,1.4,1.2S3.9,17.85,3.9,17.1z M17,19h4v-4c-4.63,0-9,4.37-9,9h4C16,21.41,14.93,19,17,19z M12,10v4c3.59,0,6.5,2.91,6.5,6.5h4C22.5,14.09,17.91,10,12,10z" /></svg>'
    # Icona GitHub SVG (giallo)
    github_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending RSS {lightning_svg}</title>
    <link rel="icon" type="image/png" href="https://github.githubassets.com/favicons/favicon-dark.png"> <!-- Icona scura -->
    <style>
        :root {{
            --bg-color: #1a1a1a; /* Sfondo principale scuro */
            --card-bg: #2c2c2c; /* Sfondo card leggermente più chiaro */
            --text-color: #e0e0e0; /* Testo chiaro */
            --title-color: #ffffff; /* Titoli bianchi */
            --accent-color: #ffd700; /* Giallo oro per accenti */
            --accent-hover: #ffec80; /* Giallo più chiaro per hover */
            --border-color: #444444; /* Bordi scuri */
            --card-shadow: 0 4px 15px rgba(0,0,0,0.4);
            --card-radius: 8px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
        }}

        header {{
            background: linear-gradient(135deg, #333 0%, #111 100%);
            color: var(--title-color);
            text-align: center;
            padding: 2.5rem 1rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
            border-bottom: 3px solid var(--accent-color);
        }}

        /* Animazione fulmine sottile (opzionale) */
        header::before {{
            content: '';
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            background: linear-gradient(to right, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0) 10%, rgba(255, 215, 0, 0) 90%, rgba(255, 215, 0, 0.1));
            animation: lightning-flash 5s linear infinite;
            opacity: 0.5;
            pointer-events: none;
        }}

        @keyframes lightning-flash {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}

        h1 {{
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            position: relative;
            color: var(--accent-color); /* Titolo principale giallo */
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }}
        h1 svg {{ /* Stile per SVG nel titolo */
             vertical-align: middle;
             margin-left: 10px;
             width: 1.8rem;
             height: 1.8rem;
        }}

        .build-info {{
            font-size: 0.9rem;
            margin-top: 1rem;
            color: rgba(224, 224, 224, 0.8);
            position: relative;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Grid per le card dei linguaggi */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 3rem; /* Spazio prima della sezione repo popolari */
        }}

        .language-card {{
            background: var(--card-bg);
            border-radius: var(--card-radius);
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border-color);
            padding: 25px;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .language-card:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            border-color: var(--accent-color);
        }}

        .language-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--title-color);
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 10px;
            display: inline-block;
        }}

        .feed-links {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .feed-link {{
            display: inline-flex; /* Usa flex per allineare icona e testo */
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            background-color: var(--bg-color);
            color: var(--accent-color);
            text-decoration: none;
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
            font-weight: 500;
        }}

        .feed-link:hover {{
            background-color: var(--accent-color);
            color: var(--bg-color); /* Testo scuro su sfondo giallo */
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
            border-color: var(--accent-hover);
        }}

        .rss-icon svg {{
            width: 14px;
            height: 14px;
            margin-right: 6px;
            vertical-align: middle;
            fill: currentColor; /* L'icona prende il colore del link */
        }}

        /* Sezione Repository Popolari */
        .popular-repos {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }}

        .popular-repos h2 {{
            text-align: center;
            font-size: 2rem;
            color: var(--title-color);
            margin-bottom: 2rem;
        }}
        .popular-repos h2 svg {{ /* Icona stella nel titolo */
             vertical-align: middle;
             margin-right: 10px;
             color: var(--accent-color);
        }}

        .popular-grid {{
             display: grid;
             grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
             gap: 25px;
        }}

        .popular-repo-card {{
            background: var(--card-bg);
            border-radius: var(--card-radius);
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border-color);
            padding: 20px;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
         .popular-repo-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            border-color: var(--accent-color);
        }}

        .popular-repo-card .repo-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--title-color);
            margin-bottom: 10px;
            word-break: break-all; /* Evita overflow nomi lunghi */
        }}
        .popular-repo-card .repo-title a {{
            color: inherit;
            text-decoration: none;
        }}
         .popular-repo-card .repo-title a:hover {{
            color: var(--accent-color);
            text-decoration: underline;
        }}

        .popular-repo-card .repo-description {{
            font-size: 0.95rem;
            color: var(--text-color);
            margin-bottom: 15px;
            flex-grow: 1; /* Fa espandere la descrizione */
        }}

        .popular-repo-card .repo-stats {{
            font-size: 0.9rem;
            color: var(--text-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto; /* Spinge le stats in basso */
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
        }}
        .popular-repo-card .repo-stats span {{
             display: inline-flex;
             align-items: center;
             gap: 5px;
        }}
        .popular-repo-card .repo-stats .stars svg {{ color: var(--accent-color); }} /* Stella gialla */


        /* Footer */
        footer {{
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            background-color: #111; /* Footer molto scuro */
            border-top: 1px solid var(--border-color);
            color: var(--text-color);
        }}

        footer a {{
            color: var(--accent-color);
            text-decoration: none;
        }}

        footer a:hover {{
            color: var(--accent-hover);
            text-decoration: underline;
        }}

        .footer-content {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 10px;
        }}

        .github-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .github-icon svg {{
            width: 20px;
            height: 20px;
            fill: currentColor;
        }}

        @media (max-width: 768px) {{
            .cards-grid, .popular-grid {{
                grid-template-columns: 1fr; /* Una colonna su mobile */
            }}

            h1 {{
                font-size: 2.2rem;
            }}
             .popular-repos h2 {{
                 font-size: 1.8rem;
             }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{lightning_svg} GitHub Trending RSS</h1>
            <div class="build-info">Ultimo aggiornamento: {build_date}</div>
        </div>
    </header>

    <div class="container">
        <div class="cards-grid">
            <!-- Qui verranno inserite le card dei linguaggi -->
        </div>

        <div class="popular-repos">
             <h2><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="1em" height="1em"><path d="M12,17.27L18.18,21L17,14.64L22,9.73L14.81,8.63L12,2L9.19,8.63L2,9.73L7,14.64L5.82,21L12,17.27Z"/></svg> Repository Popolari del Mese</h2>
             <div class="popular-grid">
                <!-- Qui verranno inseriti gli esempi di repo popolari -->
             </div>
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <p>Generato automaticamente con Python {lightning_svg}</p>
            <a href="https://github.com/duccioo/GitHubTrendingRSS" class="github-link" target="_blank" rel="noopener noreferrer">
                <span class="github-icon">{github_svg}</span>
                Codice Sorgente su GitHub
            </a>
        </div>
    </footer>
</body>
</html>
"""
