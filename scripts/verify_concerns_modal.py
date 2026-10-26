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

dash_html_fixed = dash_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

# Inject a small script to test opening the modal via #moreConcernsBtn
modal_test_script = """
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const moreBtn = document.getElementById('moreConcernsBtn');
        if (moreBtn) {
            moreBtn.click();
            console.log('Clicked moreConcernsBtn, modal active:', document.getElementById('concernsModalBackdrop').classList.contains('is-open'));
        }
    }, 100);
});
</script>
</body>
"""
test_html = dash_html_fixed.replace('</body>', modal_test_script)

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
modal_html_path = os.path.join(artifact_dir, "temp_modal_test.html")
modal_shot = os.path.join(artifact_dir, "concerns_modal_open.png")

with open(modal_html_path, "w", encoding="utf-8") as f:
    f.write(test_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    "--window-size=1440,1050",
    f"--screenshot={modal_shot}",
    modal_html_path
]
subprocess.run(cmd, check=True)
print("Captured modal screenshot:", modal_shot)
