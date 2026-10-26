import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

artifacts_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\76f5aa4f-e99a-4043-a04f-dfb778299c01"
scratch_dir = os.path.join(artifacts_dir, 'scratch')
os.makedirs(scratch_dir, exist_ok=True)
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

static_abs = "file:///d:/smart appointment manager/app/static/"

app = create_app()
with app.test_client() as client:
    # 1. Fetch Landing Page
    landing_html = client.get('/').data.decode('utf-8')
    landing_html = landing_html.replace('href="/static/', f'href="{static_abs}')
    landing_html = landing_html.replace('src="/static/', f'src="{static_abs}')
    landing_file = os.path.join(scratch_dir, 'final_landing.html')
    with open(landing_file, 'w', encoding='utf-8') as f:
        f.write(landing_html)

    # 2. Fetch Public Medications Catalog
    meds_html = client.get('/medications').data.decode('utf-8')
    meds_html = meds_html.replace('href="/static/', f'href="{static_abs}')
    meds_html = meds_html.replace('src="/static/', f'src="{static_abs}')
    meds_file = os.path.join(scratch_dir, 'final_meds.html')
    with open(meds_file, 'w', encoding='utf-8') as f:
        f.write(meds_html)

    # 3. Fetch Public Hospital Locator
    hosp_html = client.get('/hospital_locator?city=Jaipur').data.decode('utf-8')
    hosp_html = hosp_html.replace('href="/static/', f'href="{static_abs}')
    hosp_html = hosp_html.replace('src="/static/', f'src="{static_abs}')
    hosp_file = os.path.join(scratch_dir, 'final_hosp.html')
    with open(hosp_file, 'w', encoding='utf-8') as f:
        f.write(hosp_html)

# Take screenshots
shot_landing = os.path.join(artifacts_dir, "landing_verified.png")
shot_meds = os.path.join(artifacts_dir, "medications_verified.png")
shot_hosp = os.path.join(artifacts_dir, "hospital_locator_verified.png")

user_data = os.path.join(scratch_dir, "chrome_profile")

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    f"--user-data-dir={user_data}",
    "--window-size=1366,1600",
    f"--screenshot={shot_landing}",
    f"file:///{landing_file.replace(os.sep, '/')}"
], check=True)
print("Saved landing screenshot:", shot_landing)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    f"--user-data-dir={user_data}",
    "--window-size=1366,1600",
    f"--screenshot={shot_meds}",
    f"file:///{meds_file.replace(os.sep, '/')}"
], check=True)
print("Saved meds screenshot:", shot_meds)

subprocess.run([
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--virtual-time-budget=2000",
    f"--user-data-dir={user_data}",
    "--window-size=1366,1600",
    f"--screenshot={shot_hosp}",
    f"file:///{hosp_file.replace(os.sep, '/')}"
], check=True)
print("Saved hosp screenshot:", shot_hosp)
