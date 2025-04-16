# 🚀 GitHub Trending RSS

A Python tool that generates RSS/Atom feeds for GitHub trending repositories.

## 📋 Overview

This project is a fork of [mshibanami/GitHubTrendingRSS](https://github.com/mshibanami/GitHubTrendingRSS) reimplemented in Python for a simpler, faster approach. It fetches trending repositories from GitHub and converts them into RSS/Atom feeds that can be consumed by any feed reader.

The feeds are generated for different programming languages and time periods (daily, weekly, monthly) and are stored in a simple HTML interface for easy browsing.
The main goal is to provide a lightweight and efficient way to keep track of trending repositories on GitHub without the need for complex setups or heavy dependencies.

## ✨ Features

- 📊 Generates Atom feeds for different programming languages
- 🗓️ Supports daily, weekly, and monthly trending periods
- 🌐 Creates a simple HTML interface to browse available feeds
- 🔧 Easy to deploy and maintain
- 🪶 Minimal dependencies

## 📦 Requirements

- 🐍 Python 3.6+
- 📚 Required Python packages:
  - requests
  - python-dateutil
  - python-dotenv
  - BeautifulSoup4

## 🔧 Installation

1. Clone this repository:
   ```
   git clone https://github.com/duccioo/GitHubTrendingRSS.git
   cd GitHubTrendingRSS
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your GitHub token (optional but recommended to avoid API rate limits):
   ```
   REPO_GITHUB_TOKEN=your_github_token_here
   ```

## 🚀 Usage

Run the main script to generate all feeds and the HTML interface:

```
python src/main.py
```

This will:
1. 🔍 Fetch trending repositories from GitHub
2. 🔄 Generate Atom feeds for each language and time period
3. 🎨 Create an HTML interface to browse the feeds
4. 💾 Save everything in the appropriate directories

## 📡 Feed URLs

After running the script, feed files will be available in the `feeds` directory with the following naming convention:

```
feeds/{language_name}_{period}.xml
```

For example:
- `feeds/all_languages_daily.xml`
- `feeds/python_weekly.xml` 
- `feeds/javascript_monthly.xml`

## 🌐 Deployment

You can deploy this on any web server or hosting service that supports static sites. Simply copy the generated `index.html` and `feeds` directory to your server.

For automated updates, consider setting up a cron job or scheduled task to run the script periodically.

## TODO

- [ ] Create a Telegraph page for the README
   - [ ] Also embed the Gitstar within the Telegraph page
- [ ] Set the RSS feed link to a Telegraph page containing the nicely rendered README
- [ ] Improve the web page by adding a logo and enhancing the colors

## 📜 License

MIT

## 👏 Acknowledgements

- 🙌 Original project by [mshibanami](https://github.com/mshibanami/GitHubTrendingRSS)
- 🐙 GitHub for providing the API

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.