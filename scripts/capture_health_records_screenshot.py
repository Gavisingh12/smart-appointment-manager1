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
html_path = os.path.join(artifact_dir, "temp_health_records_preview.html")
shot_path = os.path.join(artifact_dir, "health_records_fixed.png")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(page_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1100",
    f"--screenshot={shot_path}",
    html_path
], check=True)

print("Health records screenshot saved to:", shot_path)
