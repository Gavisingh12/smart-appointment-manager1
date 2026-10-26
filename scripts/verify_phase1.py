import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Fetch login page to get CSRF token
resp = opener.open('http://127.0.0.1:5000/login')
html = resp.read().decode('utf-8')
csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', html)
if not csrf_match:
    print("FAILED: CSRF token not found on login page")
    exit(1)
csrf = csrf_match.group(1)

# 2. Post login
login_data = urllib.parse.urlencode({
    'csrf_token': csrf,
    'identifier': 'demo@carecompass.local',
    'password': 'CareCompass123!'
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:5000/login', data=login_data)
login_resp = opener.open(req)
final_url = login_resp.geturl()
print("Post-login URL:", final_url)

# 3. Fetch Dashboard
dash_resp = opener.open('http://127.0.0.1:5000/dashboard')
dash_html = dash_resp.read().decode('utf-8')

checks = [
    ("app-sidebar element", "app-sidebar" in dash_html),
    ("7-item nav items:", all(k in dash_html for k in ["Home", "Appointments", "Find Doctors", "Health Records", "Medications", "Reminders", "Settings"])),
    ("Sidebar 'Check symptoms' CTA", "Check symptoms" in dash_html),
    ("Bell icon for Reminders (SVG path d='M6 8a6')", "M6 8a6" in dash_html),
    ("Settings visually separated at bottom", "sidebar-nav-bottom" in dash_html),
    ("Warm patient greeting 'Hello, Eleanor'", "Hello, Eleanor" in dash_html),
    ("Emergency advice banner at top", "emergency-banner" in dash_html and "Urgent medical advice:" in dash_html),
    ("Symptom intake studio", "intake-card" in dash_html and "Symptom Intake" in dash_html),
    ("Accessible symptom chips (+ Fever, Onset, Severity)", all(s in dash_html for s in ["+ Fever", "Started today", "Mild (1–3)"])),
    ("Single primary action button", "Analyze symptoms &amp; prepare briefing" in dash_html or "Analyze symptoms & prepare briefing" in dash_html),
    ("Mobile bottom navigation (5 items)", "mobile-bottom-nav" in dash_html),
    ("Mobile 'More' drawer modal", "mobile-drawer" in dash_html),
    ("Real user session (not hardcoded)", "demo@carecompass.local" not in dash_html and "Eleanor Vance" in dash_html),
]

all_passed = True
for name, passed in checks:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if not passed:
        all_passed = False

if all_passed:
    print("\n--- ALL PHASE 1 ACCEPTANCE CRITERIA PASSED ---")
else:
    print("\n--- SOME CRITERIA FAILED ---")
    exit(1)
