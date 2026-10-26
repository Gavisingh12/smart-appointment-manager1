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

# 2. Fetch authenticated hospital-locator page
locator_html = opener.open('http://127.0.0.1:5000/hospital-locator').read().decode('utf-8')

locator_html_fixed = locator_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
locator_html_fixed = locator_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
locator_html_fixed = locator_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
html_path = os.path.join(artifact_dir, "temp_locator_preview.html")
shot_path = os.path.join(artifact_dir, "find_doctors_preview.png")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(locator_html_fixed)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1000",
    f"--screenshot={shot_path}",
    html_path
], check=True)

print("Locator screenshot saved successfully to:", shot_path)

# 3. Also capture scrolled state where user scrolled cards list down to Narayana & Fortis
scrolled_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const list = document.querySelector('.finder-cards-list');
        if (list) {
            list.scrollTop = 420;
        }
    }, 250);
});
</script>
</body>
"""
html_scrolled = locator_html_fixed.replace('</body>', scrolled_script)
html_scrolled_path = os.path.join(artifact_dir, "temp_locator_scrolled.html")
shot_scrolled_path = os.path.join(artifact_dir, "find_doctors_scrolled.png")

with open(html_scrolled_path, "w", encoding="utf-8") as f:
    f.write(html_scrolled)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1000",
    f"--screenshot={shot_scrolled_path}",
    html_scrolled_path
], check=True)

print("Scrolled locator screenshot saved successfully to:", shot_scrolled_path)
