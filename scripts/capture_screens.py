import subprocess
import os
import time
import shutil

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_dir = os.path.abspath(r".chrome_temp_profile")

if os.path.exists(profile_dir):
    try:
        shutil.rmtree(profile_dir)
    except Exception:
        pass

os.makedirs(profile_dir, exist_ok=True)
print("Profile dir created:", profile_dir)
