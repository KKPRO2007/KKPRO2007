import os
import requests

# -------------------------------
# CONFIG
# -------------------------------
USERNAME = "KKPRO2007"
README_PATH = "README.md"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("❌ Please set your GITHUB_TOKEN environment variable.")

headers = {"Authorization": f"token {TOKEN}"}

# -------------------------------
# FETCH REPOS (INCLUDE PRIVATE)
# -------------------------------
repos_url = f"https://api.github.com/user/repos?per_page=100&type=all"
response = requests.get(repos_url, headers=headers)
if response.status_code != 200:
    print("❌ Error fetching repos:", response.json())
    exit()

repos = response.json()
print(f"✅ Found {len(repos)} repositories")

# -------------------------------
# CALCULATE TOP LANGUAGES
# -------------------------------
lang_totals = {}

for repo in repos:
    repo_name = repo["name"]
    lang_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    lang_response = requests.get(lang_url, headers=headers)
    if lang_response.status_code == 200:
        langs = lang_response.json()
        for lang, bytes_count in langs.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count

if not lang_totals:
    print("⚠️ No language data found.")
    exit()

# Sort by usage
sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)
top_langs = [f"{lang}" for lang, _ in sorted_langs[:6]]
print("🏆 Top Languages:", ", ".join(top_langs))

# -------------------------------
# UPDATE README
# -------------------------------
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!--START_SECTION:top_langs-->"
end_tag = "<!--END_SECTION:top_langs-->"

new_section = f"{start_tag}\n**Top Languages (Including Private Repos):**\n\n" + \
              " | ".join(top_langs) + f"\n{end_tag}"

if start_tag in content and end_tag in content:
    old_section = content.split(start_tag)[1].split(end_tag)[0]
    content = content.replace(f"{start_tag}{old_section}{end_tag}", new_section)
else:
    content += "\n\n" + new_section

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ README updated successfully!")
