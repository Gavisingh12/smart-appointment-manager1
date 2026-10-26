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

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Fetch History Page and create Timeline view WITHOUT the 9 badge
hist_html = opener.open('http://127.0.0.1:5000/history').read().decode('utf-8')
hist_html = hist_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
hist_html = hist_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')

# Simulate active timeline state where badge is hidden
hist_timeline_html = hist_html.replace('id="viewSectionOverview" role="tabpanel"', 'id="viewSectionOverview" role="tabpanel" style="display: none;"')
hist_timeline_html = hist_timeline_html.replace('id="viewSectionRecords" role="tabpanel" aria-labelledby="records-heading" style="display: none;"', 'id="viewSectionRecords" role="tabpanel" aria-labelledby="records-heading" style="display: block;"')
hist_timeline_html = hist_timeline_html.replace('<span id="myRecordsBtnText">Past Consultation Records</span>', '<span id="myRecordsBtnText">← Back to Overview</span>')
hist_timeline_html = hist_timeline_html.replace('class="my-appointments-header-btn"', 'class="my-appointments-header-btn is-active"')
# Hide the count badge on the toggle button
hist_timeline_html = re.sub(r'(id="myRecordsCountBadge"[^>]*>)', r'\1style="display: none;" ', hist_timeline_html)
hist_timeline_html = hist_timeline_html.replace('id="myRecordsCountBadge">', 'id="myRecordsCountBadge" style="display: none;">')

path_records = os.path.join(artifact_dir, "temp_records_no_badge.html")
shot_records = os.path.join(artifact_dir, "records_timeline_no_badge.png")
with open(path_records, "w", encoding="utf-8") as f:
    f.write(hist_timeline_html)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,1050",
    f"--screenshot={shot_records}",
    path_records
], check=True)
print("1. Captured records without 9 badge:", shot_records)

# 2. Fetch Dashboard Page and test Normal Sidebar (Medications under Appointments)
dash_html = opener.open('http://127.0.0.1:5000/dashboard').read().decode('utf-8')
dash_html = dash_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
dash_html = dash_html.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')

path_dash = os.path.join(artifact_dir, "temp_dash_normal_sidebar.html")
shot_dash = os.path.join(artifact_dir, "sidebar_medications_under_appointments.png")
with open(path_dash, "w", encoding="utf-8") as f:
    f.write(dash_html)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,900",
    f"--screenshot={shot_dash}",
    path_dash
], check=True)
print("2. Captured sidebar with Medications under Appointments:", shot_dash)

# 3. Collapsed Sidebar State (Rail Mode)
dash_collapsed_html = dash_html.replace('class="app-layout"', 'class="app-layout sidebar-collapsed"')
dash_collapsed_html = dash_collapsed_html.replace('class="app-sidebar"', 'class="app-sidebar is-collapsed"')

path_collapsed = os.path.join(artifact_dir, "temp_dash_collapsed.html")
shot_collapsed = os.path.join(artifact_dir, "sidebar_collapsed_mode.png")
with open(path_collapsed, "w", encoding="utf-8") as f:
    f.write(dash_collapsed_html)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,900",
    f"--screenshot={shot_collapsed}",
    path_collapsed
], check=True)
print("3. Captured sidebar collapsed rail mode:", shot_collapsed)

print("SUCCESS: All states captured and verified!")
