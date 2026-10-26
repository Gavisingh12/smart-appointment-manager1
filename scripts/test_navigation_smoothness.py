import urllib.request
import urllib.parse
import http.cookiejar
import re

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

# Set cookie in CookieJar
cookie = http.cookiejar.Cookie(
    version=0, name='cc_sidebar_collapsed', value='1',
    port=None, port_specified=False,
    domain='127.0.0.1', domain_specified=True, domain_initial_dot=False,
    path='/', path_specified=True,
    secure=False, expires=None, discard=True, comment=None,
    comment_url=None, rest={'HttpOnly': None}, rfc2109=False
)
cj.set_cookie(cookie)

col_html = opener.open('http://127.0.0.1:5000/appointment').read().decode('utf-8')
print("Class in HTML:", [line.strip() for line in col_html.splitlines() if 'app-layout' in line])
assert 'sidebar-collapsed' in col_html
assert 'app-sidebar is-collapsed' in col_html
print("[PASS] Authenticated request with cookie renders sidebar-collapsed server-side!")
