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

# 2. Fetch authenticated dashboard HTML
dash_html = opener.open('http://127.0.0.1:5000/dashboard').read().decode('utf-8')

# Ensure asset URLs point to absolute local server so headless chrome loads them properly
dash_html_fixed = dash_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
top_html_path = os.path.join(artifact_dir, "temp_dashboard_top.html")
scrolled_html_path = os.path.join(artifact_dir, "temp_dashboard_scrolled.html")

with open(top_html_path, "w", encoding="utf-8") as f:
    f.write(dash_html_fixed)

# Add immediate scroll script to test sticky/fixed sidebar behavior
scrolled_html = dash_html_fixed.replace(
    '</body>',
    '<script>document.documentElement.scrollTop = 450; document.body.scrollTop = 450;</script></body>'
)
with open(scrolled_html_path, "w", encoding="utf-8") as f:
    f.write(scrolled_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
top_shot = os.path.join(artifact_dir, "dashboard_verified_top.png")
scrolled_shot = os.path.join(artifact_dir, "dashboard_verified_scrolled.png")

# Take full page screenshot
cmd1 = [
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1400",
    f"--screenshot={top_shot}",
    top_html_path
]
subprocess.run(cmd1, check=True)
print("Captured full page screenshot:", top_shot)

# Take scrolled screenshot
cmd2 = [
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,900",
    "--virtual-time-budget=1000",
    f"--screenshot={scrolled_shot}",
    scrolled_html_path
]
subprocess.run(cmd2, check=True)
print("Captured scrolled screenshot:", scrolled_shot)
