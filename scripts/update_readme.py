import os
import requests

USERNAME = os.getenv("GITHUB_USER")
TOKEN = os.getenv("GH_TOKEN")

# Fetch all repos
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
repos = requests.get(url, auth=(USERNAME, TOKEN)).json()

lang_totals = {}
for repo in repos:
    repo_name = repo["name"]
    lang_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    langs = requests.get(lang_url, auth=(USERNAME, TOKEN)).json()
    for lang, bytes_count in langs.items():
        lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count

# Sort languages by bytes
top_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:10]

# Generate markdown
markdown = ""
for lang, bytes_count in top_langs:
    markdown += f"- **{lang}**: {bytes_count} bytes\n"

# Update README.md (replace placeholder)
with open("README.md", "r") as f:
    content = f.read()

start_marker = "<!--LANGUAGES_START-->"
end_marker = "<!--LANGUAGES_END-->"

new_content = content.split(start_marker)[0] + start_marker + "\n" + markdown + end_marker + content.split(end_marker)[1]

with open("README.md", "w") as f:
    f.write(new_content)
