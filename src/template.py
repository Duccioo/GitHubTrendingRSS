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
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending RSS</title>
    <link rel="icon" type="image/png" href="https://github.githubassets.com/favicons/favicon.png">
    <style>
        :root {{
            --primary-color: #2188ff;
            --primary-dark: #0366d6;
            --secondary-color: #24292e;
            --accent-color: #28a745;
            --text-color: #24292e;
            --light-text: #6a737d;
            --lighter-bg: #f6f8fa;
            --card-shadow: 0 3px 10px rgba(0,0,0,0.1);
            --card-border: 1px solid #e1e4e8;
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
            background-color: var(--lighter-bg);
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path fill="rgba(255,255,255,0.05)" d="M0 0 L100 0 L100 100 Z"></path></svg>');
            background-size: cover;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin: 0;
            position: relative;
        }}
        
        .build-info {{
            font-size: 0.9rem;
            margin-top: 0.75rem;
            color: rgba(255,255,255,0.85);
            position: relative;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        
        .language-card {{
            background: white;
            border-radius: var(--card-radius);
            box-shadow: var(--card-shadow);
            border: var(--card-border);
            padding: 25px;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .language-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }}
        
        .language-title {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--primary-dark);
            border-bottom: 2px solid var(--primary-color);
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
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            background-color: var(--lighter-bg);
            color: var(--primary-dark);
            text-decoration: none;
            border: 1px solid #e1e4e8;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .feed-link:hover {{
            background-color: var(--primary-dark);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .rss-icon {{
            display: inline-block;
            width: 14px;
            height: 14px;
            margin-right: 5px;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M6,19h4C10,14.37,5.63,10,1,10v4C3.59,14,6,16.41,6,19z M3.9,17.1C3.9,16.36,3.26,15.9,2.5,15.9s-1.4,0.46-1.4,1.2s0.63,1.2,1.4,1.2S3.9,17.85,3.9,17.1z M17,19h4v-4c-4.63,0-9,4.37-9,9h4C16,21.41,14.93,19,17,19z M12,10v4c3.59,0,6.5,2.91,6.5,6.5h4C22.5,14.09,17.91,10,12,10z" /></svg>');
            background-size: contain;
            vertical-align: middle;
        }}
        
        .github-badge {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            gap: 10px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .badge-dark {{
            background-color: var(--secondary-color);
            color: white;
        }}
        
        .badge-light {{
            background-color: white;
            color: var(--secondary-color);
            border: 1px solid #e1e4e8;
        }}
        
        .passing {{
            color: var(--accent-color);
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            background-color: white;
            border-top: 1px solid #e1e4e8;
        }}
        
        footer a {{
            color: var(--primary-dark);
            text-decoration: none;
        }}
        
        footer a:hover {{
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
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .github-icon {{
            width: 20px;
            height: 20px;
        }}
        
        @media (max-width: 768px) {{
            .cards-grid {{
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            }}
            
            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>GitHub Trending RSS</h1>
            <div class="github-badge">
                <span class="badge badge-dark">Feeds aggiornati</span>
                <span class="badge badge-light">★ Star on GitHub</span>
            </div>
            <div class="build-info">Ultimo aggiornamento: {build_date}</div>
        </div>
    </header>
    
    <div class="container">
        <div class="cards-grid">
            <!-- Qui verranno inserite le card dei linguaggi -->
        </div>
    </div>
    
    <footer>
        <div class="footer-content">
            <p>Generato automaticamente con Python</p>
            <a href="https://github.com/duccioo/GitHubTrendingRSS" class="github-link">
                <svg class="github-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                Codice sorgente
            </a>
        </div>
    </footer>
</body>
</html>
"""
