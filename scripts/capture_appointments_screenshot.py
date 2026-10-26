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

# 2. Fetch authenticated appointments page
app_html = opener.open('http://127.0.0.1:5000/appointment').read().decode('utf-8')

app_html_fixed = app_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
app_html_fixed = app_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
app_html_fixed = app_html_fixed.replace('data-image="/static/', 'data-image="http://127.0.0.1:5000/static/')
app_html_fixed = app_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")


artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
html_path_init = os.path.join(artifact_dir, "temp_appointment_init.html")
shot_path_init = os.path.join(artifact_dir, "appointment_initial_state.png")

# State 1: All Specialists Initial View
with open(html_path_init, "w", encoding="utf-8") as f:
    f.write(app_html_fixed)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1100",
    f"--screenshot={shot_path_init}",
    html_path_init
], check=True)
print("Initial state screenshot saved to:", shot_path_init)

# State 2: General Physician Selected (Show updated Knowledge Banner + 5 doctors)
physician_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const physBtn = document.querySelector('[data-dept="physician"]');
        if (physBtn) physBtn.click();
    }, 200);
});
</script>
</body>
"""
html_phys = app_html_fixed.replace('</body>', physician_script)
html_path_phys = os.path.join(artifact_dir, "temp_appointment_phys.html")
shot_path_phys = os.path.join(artifact_dir, "appointment_physician_selected.png")

with open(html_path_phys, "w", encoding="utf-8") as f:
    f.write(html_phys)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    "--window-size=1440,1100",
    f"--screenshot={shot_path_phys}",
    html_path_phys
], check=True)
print("Physician selected state screenshot saved to:", shot_path_phys)

# State 3: More Specialties Dropdown Open
dropdown_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const moreBtn = document.getElementById('moreDeptToggleBtn');
        if (moreBtn) moreBtn.click();
    }, 200);
});
</script>
</body>
"""
html_dd = app_html_fixed.replace('</body>', dropdown_script)
html_path_dd = os.path.join(artifact_dir, "temp_appointment_dd.html")
shot_path_dd = os.path.join(artifact_dir, "appointment_dropdown_opened.png")

with open(html_path_dd, "w", encoding="utf-8") as f:
    f.write(html_dd)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    "--window-size=1440,1100",
    f"--screenshot={shot_path_dd}",
    html_path_dd
], check=True)
print("Dropdown open screenshot saved to:", shot_path_dd)



