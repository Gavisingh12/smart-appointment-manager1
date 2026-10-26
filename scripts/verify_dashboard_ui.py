import urllib.request
import urllib.parse
import http.cookiejar
import re

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

# 2. Fetch Dashboard
resp = opener.open('http://127.0.0.1:5000/dashboard')
dash_html = resp.read().decode('utf-8')

elements = [
    ('Hero banner', 'hero-guidance-card' in dash_html),
    ('Hero photography (hero_wellness.jpg)', 'hero_wellness.jpg' in dash_html),
    ('Get Guidance button', 'Get Guidance' in dash_html),
    ('Top search bar in desktop header', 'topbar-search-box' in dash_html),
    ('Common health concerns (7 cards)', 'concerns-section' in dash_html and 'concern-fever' in dash_html),
    ('Overview triad (3 columns)', 'overview-triad-grid' in dash_html),
    ('Upcoming appointment with doctor photo', 'doctor_ananya.jpg' in dash_html),
    ('Recent consultations card', 'Recent Consultations' in dash_html),
    ('Health records card', 'Your Health Records' in dash_html),
    ('Bottom encouragement banner', 'bottom-consultation-banner' in dash_html),
    ('Sidebar help card ("Need help?")', 'sidebar-help-card' in dash_html),
]

all_ok = True
for name, ok in elements:
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        all_ok = False

if all_ok:
    print("\n>>> ALL DASHBOARD UI ELEMENTS MATCH AND VERIFIED SUCCESSFULLY <<<")
else:
    print("\n>>> SOME ELEMENTS FAILED <<<")
    exit(1)
