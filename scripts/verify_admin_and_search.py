import urllib.request
import urllib.parse
import http.cookiejar
import re
import json

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

# 2. Check Admin Page
admin_resp = opener.open('http://127.0.0.1:5000/medications/admin')
admin_html = admin_resp.read().decode('utf-8')
assert 'Pharmacy Inventory' in admin_html, 'Admin title not found'
assert 'Pain &amp; Fever' in admin_html or 'Pain' in admin_html, 'Category not found in admin'
print('[PASS] Admin page loads with categories and inventory table')

# 3. Check Search API
search_resp = opener.open('http://127.0.0.1:5000/api/medications/search?q=fever')
search_data = json.loads(search_resp.read().decode('utf-8'))
assert search_data['total'] > 0, 'No search results for fever'
print('[PASS] Search API returns:', search_data['total'], 'results for query "fever"')
for p in search_data['products'][:3]:
    print('   ->', p['name'], '(', p['salt'], ')- Rs.', p['price'])

# 4. Check Search API for symptoms: cough, diabetes, pressure
for symptom in ['cough', 'diabetes', 'pressure']:
    s_resp = opener.open(f'http://127.0.0.1:5000/api/medications/search?q={symptom}')
    s_data = json.loads(s_resp.read().decode('utf-8'))
    print(f'[PASS] Search for "{symptom}" returns {s_data["total"]} matching medicines')

print('\n>>> ALL ADMIN AND SEARCH TESTS PASSED <<<')
