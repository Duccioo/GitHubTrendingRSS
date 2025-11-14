"""
This module contains the HTML template for the GitHubTrendingRSS website.
"""


def get_html_template(build_date):
    """
    Returns the HTML template with the specified build date.

    Parameters:
    build_date (str): Site generation date/time string

    Returns:
    str: HTML template
    """
    # Emojis (replace SVGs)
    lightning_emoji = "⚡️"
    star_emoji = "⭐"
    github_emoji = "🐙"  # Octocat emoji for GitHub link
    down_arrow_emoji = "🔽"  # Emoji for dropdown

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending RSS {lightning_emoji}</title>
    <link rel="icon" type="image/png" href="https://github.githubassets.com/favicons/favicon-dark.png">
    <style>
        :root {{
            --bg-color: #1a1a1a;
            --card-bg: #2c2c2c;
            --text-color: #e0e0e0;
            --title-color: #ffffff;
            --accent-color: #ffd700; /* Gold yellow */
            --accent-hover: #ffec80;
            --border-color: #444444;
            --card-shadow: 0 4px 15px rgba(0,0,0,0.4);
            --card-radius: 8px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        html {{
            scroll-behavior: smooth; /* Enable smooth scrolling */
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            font-size: 16px; /* Base font size */
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

        /* Optional subtle flash animation */
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
            margin: 0 0 0.5rem 0; /* Added bottom margin */
            position: relative;
            color: var(--accent-color); /* Main title yellow */
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }}
        /* Emoji in title might not need specific styling unless alignment is off */

        .header-links {{ /* Container for links below title */
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }}

        .header-links a {{
            color: var(--accent-hover);
            text-decoration: none;
            margin: 0 10px;
            font-size: 1rem;
            transition: color 0.2s ease;
        }}

        .header-links a:hover {{
            color: var(--accent-color);
            text-decoration: underline;
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

        /* Section Titles */
        h2 {{
            text-align: center;
            font-size: 2rem;
            color: var(--title-color);
            margin-bottom: 2rem;
            margin-top: 3rem; /* Add space above section titles */
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}
         h2 .emoji {{ /* Style for emoji in H2 */
             margin-right: 10px;
             vertical-align: middle; /* Better alignment */
        }}

        /* Main Languages Section */
        .main-languages-section {{
            margin-bottom: 3rem;
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: var(--card-radius);
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border-color);
        }}
        .main-languages-section h2 {{
            margin-top: 0; /* Remove top margin for h2 inside this section */
            margin-bottom: 1.5rem;
            text-align: left;
            border-bottom: none; /* Remove border for this specific h2 */
            font-size: 1.8rem;
        }}
        .main-language-group {{
            margin-bottom: 1.5rem;
        }}
        .main-language-group:last-child {{
            margin-bottom: 0;
        }}
        .main-language-group h3 {{
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--title-color);
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        /* Grid for language cards */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 3rem;
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
            justify-content: center; /* Center links in cards */
            flex-wrap: wrap;
            gap: 15px;
        }}
        /* Adjust feed links alignment for main languages section */
        .main-language-group .feed-links {{
             justify-content: flex-start; /* Align links to the start */
        }}

        .feed-link {{
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            background-color: var(--bg-color);
            color: var(--accent-color);
            text-decoration: none;
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
            font-weight: 500;
            font-size: 0.95rem; /* Slightly smaller font for links */
        }}

        .feed-link:hover {{
            background-color: var(--accent-color);
            color: var(--bg-color);
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
            border-color: var(--accent-hover);
        }}

        .feed-link .emoji {{ /* Style for emoji within link */
            margin-right: 6px;
            font-size: 1em; /* Match link font size */
            display: inline-block; /* Helps with alignment */
        }}

        /* Popular Repositories Section */
        .popular-repos {{
            margin-top: 3rem;
            /* Removed border-top, handled by h2 */
        }}

        .popular-repos h2 {{
            /* Styles already defined in general h2 */
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
            word-break: break-all;
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
            flex-grow: 1;
        }}

        .popular-repo-card .repo-stats {{
            font-size: 0.9rem;
            color: var(--text-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
        }}
        .popular-repo-card .repo-stats span {{
             display: inline-flex;
             align-items: center;
             gap: 5px;
        }}
        .popular-repo-card .repo-stats .emoji {{ /* Style for stat emojis */
             font-size: 1.1em; /* Slightly larger emoji */
             display: inline-block;
        }}

        .star-history-chart {{
            margin: 15px 0; /* Add some vertical spacing */
            text-align: center; /* Center the image if needed */
            background-color: #ffffff; /* Add a white background for better contrast */
            padding: 5px;
            border-radius: 4px;
            line-height: 0; /* Prevent extra space below the image */
        }}

        .star-history-chart img {{
            max-width: 100%; /* Ensure image scales down */
            height: auto;   /* Maintain aspect ratio */
            display: block; /* Remove potential extra space below */
            margin: 0 auto; /* Center image if container is wider */
        }}

        /* Other Languages Section */
        .other-languages-section {{
            margin-top: 3rem;
            /* Removed border-top, handled by h2 */
        }}

        .other-languages-section details {{
            background: var(--card-bg);
            border-radius: var(--card-radius);
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border-color);
            margin-bottom: 1rem; /* Space below the details block */
            overflow: hidden; /* Contain the border radius */
        }}

        .other-languages-section summary {{
            padding: 15px 20px;
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--title-color);
            cursor: pointer;
            outline: none;
            transition: background-color 0.2s ease;
            list-style: none; /* Remove default marker */
            display: flex; /* Use flexbox for alignment */
            justify-content: space-between; /* Space between text and arrow */
            align-items: center;
        }}
        .other-languages-section summary::marker, /* Hide marker for Webkit */
        .other-languages-section summary::-webkit-details-marker {{
            display: none;
        }}

        .other-languages-section summary:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}

        .other-languages-section summary .arrow {{
            font-size: 1em; /* Match summary font size */
            transition: transform 0.3s ease;
        }}

        .other-languages-section details[open] summary .arrow {{
            transform: rotate(180deg);
        }}


        .other-languages-section details .cards-grid {{
            padding: 25px;
            margin-bottom: 0; /* Remove bottom margin inside details */
            border-top: 1px solid var(--border-color); /* Separator line */
        }}


        /* Footer */
        footer {{
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            background-color: #111;
            border-top: 1px solid var(--border-color);
            color: var(--text-color);
            font-size: 0.9rem;
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
            gap: 15px; /* Increased gap */
        }}

        .footer-links {{ /* Container for multiple links */
            display: flex;
            gap: 20px;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap; /* Allow wrapping on small screens */
        }}

        .footer-link {{ /* Style for individual footer links */
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .footer-link .emoji {{ /* Emoji in footer links */
            font-size: 1.2em;
        }}

        @media (max-width: 768px) {{
            .cards-grid, .popular-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 2.2rem;
            }}
             h2 {{ /* Adjust h2 size for mobile */
                 font-size: 1.8rem;
             }}
             .main-languages-section h2 {{
                 font-size: 1.6rem; /* Slightly smaller for this specific h2 */
             }}
             .other-languages-section summary {{
                 font-size: 1.1rem;
             }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{lightning_emoji} GitHub Trending RSS</h1>
            <div class="header-links">
                <a href="#other-languages">Browse Other Languages {down_arrow_emoji}</a>
            </div>
            <div class="build-info">Last updated: {build_date}</div>
        </div>
    </header>

    <div class="container">

        <!-- Section for "New" Repositories -->
        <div class="main-languages-section">
             <h2>New Repositories</h2>
             <!-- Main language links will be inserted here -->
        </div>

        <!-- Section for "Recently Updated" Repositories -->
        <div class="main-languages-section">
            <h2>Recently Updated Repositories</h2>
            <!-- Recently updated links will be inserted here -->
        </div>

        <!-- Popular Repositories Section -->
        <div class="popular-repos">
             <h2><span class="emoji">{star_emoji}</span> Popular Repositories (Monthly)</h2>
             <div class="popular-grid">
                <!-- Popular repo examples will be inserted here -->
             </div>
        </div>

        <!-- Other Languages Section (Collapsible) -->
        <div id="other-languages" class="other-languages-section">
            <h2>Other Languages</h2>
            <details>
                <summary>
                    <span>Click to expand/collapse</span>
                    <span class="arrow">{down_arrow_emoji}</span>
                </summary>
                <div class="cards-grid">
                    <!-- Other language cards will be inserted here -->
                </div>
            </details>
        </div>

    </div>

    <footer>
        <div class="footer-content">
            <p>{lightning_emoji} Created with Love by Duccio Meconcelli {lightning_emoji}</p>
            <div class="footer-links">
                <a href="https://github.com/duccioo/GitHubTrendingRSS" class="footer-link" target="_blank" rel="noopener noreferrer">
                    <span class="emoji">{github_emoji}</span>
                    Source Code on GitHub
                </a>
                <a href="https://duccio.me" class="footer-link" target="_blank" rel="noopener noreferrer">
                    <span class="emoji">👤</span>
                    duccio.me
                </a>
            </div>
        </div>
    </footer>
</body>
</html>
"""
