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

# 2. Fetch authenticated dashboard HTML
dash_html = opener.open('http://127.0.0.1:5000/dashboard').read().decode('utf-8')

dash_html_fixed = dash_html.replace('href="/static/', 'href="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace('src="/static/', 'src="http://127.0.0.1:5000/static/')
dash_html_fixed = dash_html_fixed.replace("url('/static/", "url('http://127.0.0.1:5000/static/")

# Inject a test script that sets symptoms and triggers the loading state
test_script = """
<script>
window.addEventListener('load', () => {
    const symInput = document.getElementById('symptoms');
    const form = document.getElementById('diagnosisForm');
    const submitBtn = document.getElementById('prepare-summary-btn');
    const progressTrack = document.getElementById('intakeProgressTrack');
    const heroWrapper = document.getElementById('heroSearchWrapper');
    const feedback = document.getElementById('diagnosisFeedback');

    if (symInput) {
        symInput.value = 'Persistent dry cough, sore throat, and chest congestion';
    }

    // Trigger visual loading state
    if (progressTrack) progressTrack.classList.add('active');
    if (heroWrapper) heroWrapper.classList.add('is-loading');
    if (feedback) {
        feedback.classList.remove('hidden');
        feedback.textContent = 'Reviewing symptom observations against clinical guidelines...';
    }
    if (submitBtn) {
        submitBtn.classList.add('is-loading');
        submitBtn.innerHTML = `
            <svg class="spinner-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="12" y1="2" x2="12" y2="6"></line>
              <line x1="12" y1="18" x2="12" y2="22"></line>
              <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
              <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
              <line x1="2" y1="12" x2="6" y2="12"></line>
              <line x1="18" y1="12" x2="22" y2="12"></line>
              <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
              <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
            </svg>
            <span>Analyzing Clinical Signs...</span>
        `;
    }
});
</script>
</body>
"""

test_html = dash_html_fixed.replace('</body>', test_script)

artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"
active_html_path = os.path.join(artifact_dir, "temp_analyzing_state.html")
active_shot = os.path.join(artifact_dir, "analyzing_clinical_signs_active.png")

with open(active_html_path, "w", encoding="utf-8") as f:
    f.write(test_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--hide-scrollbars",
    "--window-size=1440,900",
    f"--screenshot={active_shot}",
    active_html_path
]
subprocess.run(cmd, check=True)
print("Captured active state screenshot:", active_shot)
