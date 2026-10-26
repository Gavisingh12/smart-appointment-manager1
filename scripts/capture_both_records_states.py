import urllib.request
import urllib.parse
import http.cookiejar
import re
import subprocess
import os

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login
resp = opener.open('http://127.0.0.1:5000/login')
html = resp.read().decode('utf-8')
csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

data = urllib.parse.urlencode({
    'csrf_token': csrf,
    'identifier': 'demo@carecompass.local',
    'password': 'CareCompass123!'
}).encode('utf-8')
opener.open(urllib.request.Request('http://127.0.0.1:5000/login', data=data))

# 2. Fetch /history page
page_html = opener.open('http://127.0.0.1:5000/history').read().decode('utf-8')
page_html = page_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
page_html = page_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
page_html = page_html.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# A. Screenshot 1: Clean Overview State
html_path_a = os.path.join(artifact_dir, "temp_records_overview.html")
shot_path_a = os.path.join(artifact_dir, "records_clean_overview.png")
with open(html_path_a, "w", encoding="utf-8") as f:
    f.write(page_html)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,950",
    f"--screenshot={shot_path_a}",
    html_path_a
], check=True)
print("Captured Overview:", shot_path_a)

# B. Screenshot 2: Records Section Active State
page_html_b = page_html.replace('id="viewSectionOverview" role="tabpanel"', 'id="viewSectionOverview" role="tabpanel" style="display: none;"')
page_html_b = page_html_b.replace('id="viewSectionRecords" role="tabpanel" aria-labelledby="records-heading" style="display: none;"', 'id="viewSectionRecords" role="tabpanel" aria-labelledby="records-heading" style="display: block;"')
page_html_b = page_html_b.replace('<span id="myRecordsBtnText">Past Consultation Records</span>', '<span id="myRecordsBtnText">← Back to Overview</span>')
page_html_b = page_html_b.replace('class="my-appointments-header-btn"', 'class="my-appointments-header-btn is-active"')

html_path_b = os.path.join(artifact_dir, "temp_records_timeline.html")
shot_path_b = os.path.join(artifact_dir, "records_timeline_active.png")
with open(html_path_b, "w", encoding="utf-8") as f:
    f.write(page_html_b)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1100",
    f"--screenshot={shot_path_b}",
    html_path_b
], check=True)
print("Captured Records Timeline:", shot_path_b)
