import os
import requests

# -------------------------------
# CONFIG
# -------------------------------
USERNAME = "KKPRO2007"
README_PATH = "README.md"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("❌ Please set your GH_TOKEN environment variable.")

headers = {"Authorization": f"token {TOKEN}"}

# -------------------------------
# FETCH REPOS
# -------------------------------
repos_url = f"https://api.github.com/user/repos?per_page=100&type=all"
response = requests.get(repos_url, headers=headers)
if response.status_code != 200:
    print("❌ Error fetching repos:", response.json())
    exit()

repos = response.json()
print(f"✅ Found {len(repos)} repositories")

# -------------------------------
# CALCULATE LANGUAGES
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

total_bytes = sum(lang_totals.values())
sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)

# -------------------------------
# CREATE LANGUAGE BAR SECTION (Updated with full CSS styling)
# -------------------------------
top_langs_html = "<!--START_SECTION:top_langs-->\n"
top_langs_html += '<div align="center" style="background:#000; padding:20px; border-radius:10px; margin:20px 0; max-width:600px; color:#fff; text-align:center; font-family:Arial,sans-serif;">\n'
top_langs_html += '  <h3 style="color:#fff; margin-bottom:20px;">Top Languages (Including Private Repos)</h3>\n'
top_langs_html += '  \n'
top_langs_html += '  <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; max-width:600px; margin:0 auto;">\n'

for lang, bytes_count in sorted_langs[:5]:
    percent = (bytes_count / total_bytes) * 100
    top_langs_html += f'    <div style="background:#111; padding:15px; border-radius:8px; text-align:left;">\n'
    top_langs_html += f'      <p style="color:#fff; margin:0 0 8px 0; font-weight:bold;">{lang} — {percent:.2f}%</p>\n'
    top_langs_html += f'      <div style="background:#333; border-radius:4px; height:8px; width:100%;">\n'
    top_langs_html += f'        <div style="background:#3382ed; height:8px; border-radius:4px; width:{percent:.2f}%;"></div>\n'
    top_langs_html += f'      </div>\n'
    top_langs_html += f'    </div>\n'

top_langs_html += '  </div>\n'
top_langs_html += '</div>\n'
top_langs_html += '<!--END_SECTION:top_langs-->'

# -------------------------------
# UPDATE README
# -------------------------------
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!--START_SECTION:top_langs-->"
end_tag = "<!--END_SECTION:top_langs-->"

if start_tag in content and end_tag in content:
    old_section = content.split(start_tag)[1].split(end_tag)[0]
    content = content.replace(f"{start_tag}{old_section}{end_tag}", top_langs_html)
else:
    content += "\n\n" + top_langs_html

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ README updated successfully with styled Top Languages!")