import urllib.request
import urllib.parse
import http.cookiejar
import re
import os
import subprocess

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login
resp = opener.open('http://127.0.0.1:5000/login')
html = resp.read().decode('utf-8')
csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

data = urllib.parse.urlencode({
    'csrf_token': csrf,
    'identifier': 'demo@carecompass.local',
    'password': 'CareCompass123!'
}).encode('utf-8')
opener.open(urllib.request.Request('http://127.0.0.1:5000/login', data=data))

# Fetch Medications with search query "fever"
meds_fever_html = opener.open('http://127.0.0.1:5000/medications?q=fever').read().decode('utf-8')
meds_fever_html = meds_fever_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
meds_fever_html = meds_fever_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
meds_fever_html = meds_fever_html.replace('url(\'/static/', 'url(\'http://127.0.0.1:5000/static/')

scratch_dir = os.path.abspath('scratch')
fever_file = os.path.join(scratch_dir, 'meds_fever_search.html')
with open(fever_file, 'w', encoding='utf-8') as f:
    f.write(meds_fever_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
artifacts_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
img_search = os.path.join(artifacts_dir, "medications_search_fever.png")

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1366,800",
    f"--screenshot={img_search}",
    f"file:///{fever_file.replace(os.sep, '/')}"
], check=True)
print("Captured search results for 'fever':", img_search)
