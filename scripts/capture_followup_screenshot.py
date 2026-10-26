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

# 2. Post symptom to trigger session matched disease
dash_resp = opener.open('http://127.0.0.1:5000/dashboard')
dash_csrf = re.search(r'name="csrf_token" value="([^"]+)"', dash_resp.read().decode('utf-8')).group(1)
post_data = urllib.parse.urlencode({
    'csrf_token': dash_csrf,
    'symptoms': 'cough and high fever with difficulty breathing and chest tightness'
}).encode('utf-8')
try:
    dash_post = opener.open(urllib.request.Request('http://127.0.0.1:5000/dashboard', data=post_data))
    print('Dashboard POST response:', dash_post.status, dash_post.geturl())
except Exception as e:
    print('POST notice:', e)

# 3. Open followup page
try:
    followup_html = opener.open('http://127.0.0.1:5000/followup').read().decode('utf-8')
    print('Followup HTML fetched, len:', len(followup_html))
    
    dash_html_fixed = followup_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
    dash_html_fixed = dash_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
    dash_html_fixed = dash_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

    artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
    html_path = os.path.join(artifact_dir, "temp_followup.html")
    
    # Inject script that clicks chip 1 and scrolls to show the new optional box
    interactive_html = dash_html_fixed.replace(
        '</body>',
        '''<script>
          window.addEventListener("load", () => {
            setTimeout(() => {
              const notesCard = document.getElementById("additional-notes-card");
              if (notesCard) {
                notesCard.scrollIntoView({ behavior: "instant", block: "center" });
              }
            }, 100);
          });
        </script></body>'''
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(interactive_html)

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    shot_path = os.path.join(artifact_dir, "followup_current_state.png")

    cmd = [
        chrome_path,
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=1440,2400",
        f"--screenshot={shot_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    print("Screenshot saved to:", shot_path)
except Exception as exc:
    print('Followup fetch error:', exc)
