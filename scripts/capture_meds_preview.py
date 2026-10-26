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

# 1. Fetch Medications Page HTML
meds_html = opener.open('http://127.0.0.1:5000/medications').read().decode('utf-8')
meds_html = meds_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
meds_html = meds_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
meds_html = meds_html.replace('url(\'/static/', 'url(\'http://127.0.0.1:5000/static/')

# 2. Fetch Admin Page HTML
admin_html = opener.open('http://127.0.0.1:5000/medications/admin').read().decode('utf-8')
admin_html = admin_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
admin_html = admin_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')

scratch_dir = os.path.abspath('scratch')
os.makedirs(scratch_dir, exist_ok=True)

meds_file = os.path.join(scratch_dir, 'meds_flipkart.html')
with open(meds_file, 'w', encoding='utf-8') as f:
    f.write(meds_html)

admin_file = os.path.join(scratch_dir, 'admin_page.html')
with open(admin_file, 'w', encoding='utf-8') as f:
    f.write(admin_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
artifacts_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\76f5aa4f-e99a-4043-a04f-dfb778299c01"

img_flipkart = os.path.join(artifacts_dir, "medications_cleaned.png")
img_admin = os.path.join(artifacts_dir, "medications_admin_panel.png")

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1366,2200",
    f"--screenshot={img_flipkart}",
    f"file:///{meds_file.replace(os.sep, '/')}"
], check=True)
print("Captured Flipkart medications page:", img_flipkart)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1366,800",
    f"--screenshot={img_admin}",
    f"file:///{admin_file.replace(os.sep, '/')}"
], check=True)
print("Captured Admin medications page:", img_admin)
