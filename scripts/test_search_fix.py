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

# Test 1: Search "new delhi" in search bar
delhi_res = opener.open('http://127.0.0.1:5000/hospital-locator?q=new+delhi').read().decode('utf-8')
print("--- TEST 1: Search 'new delhi' ---")
print("AIIMS New Delhi found:", "AIIMS New Delhi" in delhi_res)
print("Max Super Speciality found:", "Max Super Speciality" in delhi_res)
print("Count says 'Delhi, NCR':", "healthcare providers near <span class=\"highlight-city\">Delhi, NCR</span>" in delhi_res)
print("No 'Delhi, Rajasthan' glitch:", "Delhi, Rajasthan" not in delhi_res)

# Test 2: Search "Mumbai" in search bar
mumbai_res = opener.open('http://127.0.0.1:5000/hospital-locator?q=mumbai').read().decode('utf-8')
print("\n--- TEST 2: Search 'mumbai' ---")
print("Lilavati Hospital found:", "Lilavati Hospital" in mumbai_res)
print("Kokilaben Hospital found:", "Kokilaben" in mumbai_res)
print("Count says 'Mumbai, Maharashtra':", "Mumbai, Maharashtra" in mumbai_res)

# Test 3: Search "Cardiology" in search bar in Jaipur
cardio_res = opener.open('http://127.0.0.1:5000/hospital-locator?q=cardiology').read().decode('utf-8')
print("\n--- TEST 3: Search 'cardiology' in Jaipur ---")
print("Apex Multispeciality found:", "Apex Multispeciality" in cardio_res)
print("Jaipur Heart found:", "Jaipur Heart" in cardio_res)

# Test 4: Search "punjab" in search bar (even if current city is Delhi)
punjab_res = opener.open('http://127.0.0.1:5000/hospital-locator?q=punjab&city=Delhi').read().decode('utf-8')
print("\n--- TEST 4: Search 'punjab' (from Delhi) ---")
print("PGIMER found:", "PGIMER" in punjab_res)
print("Max Mohali found:", "Max Super Speciality Hospital, Mohali" in punjab_res)
print("Fortis Mohali found:", "Fortis Hospital Mohali" in punjab_res)
print("Count says 'Chandigarh, Punjab':", "Chandigarh, Punjab" in punjab_res)
print("Option Chandigarh is selected:", 'value="Chandigarh" selected' in punjab_res)

# Test 5: Search "new delhi" (even if current city is Jaipur)
new_delhi_res = opener.open('http://127.0.0.1:5000/hospital-locator?q=new+delhi&city=Jaipur').read().decode('utf-8')
print("\n--- TEST 5: Search 'new delhi' (from Jaipur) ---")
print("AIIMS New Delhi found:", "AIIMS New Delhi" in new_delhi_res)
print("Count says 'Delhi, NCR':", "Delhi, NCR" in new_delhi_res)
print("Option Delhi is selected:", 'value="Delhi" selected' in new_delhi_res)

print("\nAll search tests executed.")

