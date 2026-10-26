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

# 2. Start symptom consultation
dash_resp = opener.open('http://127.0.0.1:5000/dashboard')
dash_csrf = re.search(r'name="csrf_token" value="([^"]+)"', dash_resp.read().decode('utf-8')).group(1)
post_data = urllib.parse.urlencode({
    'csrf_token': dash_csrf,
    'symptoms': 'loss of taste alongside severe indigestion and abdominal discomfort'
}).encode('utf-8')
opener.open(urllib.request.Request('http://127.0.0.1:5000/dashboard', data=post_data))

# 3. Post to /followup with responses
followup_resp = opener.open('http://127.0.0.1:5000/followup')
followup_html = followup_resp.read().decode('utf-8')
f_csrf = re.search(r'name="csrf_token" value="([^"]+)"', followup_html).group(1)

f_data = urllib.parse.urlencode({
    'csrf_token': f_csrf,
    'response0': 'Ongoing for 2 to 3 days',
    'response1': 'No, have not experienced this',
    'response2': 'Severe distress (8/10)',
    'response3': 'Took ibuprofen / NSAID pain reliever',
    'response4': 'Noticeably worse at night'
}).encode('utf-8')

result_resp = opener.open(urllib.request.Request('http://127.0.0.1:5000/followup', data=f_data))
result_html = result_resp.read().decode('utf-8')
print('Result page HTML fetched, len:', len(result_html))

dash_html_fixed = result_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\76f5aa4f-e99a-4043-a04f-dfb778299c01"
os.makedirs(artifact_dir, exist_ok=True)
html_path = os.path.join(artifact_dir, "temp_result_page.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(dash_html_fixed)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
shot_path = os.path.join(artifact_dir, "result_fixed_state.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,2100",
    f"--screenshot={shot_path}",
    html_path
]
subprocess.run(cmd, check=True)
print("Result screenshot saved to:", shot_path)
