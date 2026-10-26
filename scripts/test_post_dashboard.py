import urllib.request
import urllib.parse
import http.cookiejar
import re
import time

cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login
html = op.open('http://127.0.0.1:5000/login').read().decode('utf-8')
csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

op.open(urllib.request.Request(
    'http://127.0.0.1:5000/login',
    data=urllib.parse.urlencode({
        'csrf_token': csrf,
        'identifier': 'demo@carecompass.local',
        'password': 'CareCompass123!'
    }).encode('utf-8')
))

# 2. Get dashboard CSRF
dash = op.open('http://127.0.0.1:5000/dashboard').read().decode('utf-8')
csrf2 = re.search(r'name="csrf_token" value="([^"]+)"', dash).group(1)

# 3. Post symptoms
symptoms = "Persistent dry cough, sore throat, and chest congestion"
t0 = time.time()
req = urllib.request.Request(
    'http://127.0.0.1:5000/dashboard',
    data=urllib.parse.urlencode({
        'csrf_token': csrf2,
        'symptoms': symptoms
    }).encode('utf-8'),
    headers={'Accept': 'application/json'}
)
res = op.open(req)
duration = time.time() - t0
print(f"Status: {res.status}, Time: {duration:.2f}s")
print(f"Response: {res.read().decode('utf-8')}")
