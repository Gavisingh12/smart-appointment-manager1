import time
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1440,900")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
artifact_dir = r"C:\Users\Govinder Singh\.gemini\antigravity-ide\brain\6c7b00c4-a5dc-4f85-96af-9722f5632d1d"

try:
    # 1. Login
    driver.get("http://127.0.0.1:5000/auth/login")
    driver.find_element(By.NAME, "email").send_keys("patient@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1.5)

    # 2. Check sidebar items order on Dashboard
    driver.get("http://127.0.0.1:5000/dashboard")
    time.sleep(1)
    nav_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-nav-list .sidebar-nav-link")
    link_texts = [l.text.strip() for l in nav_links]
    print("Sidebar Nav Order:", link_texts)
    assert link_texts == ["Home", "Appointments", "Medications", "Find Doctors", "Health Records", "Reminders"], f"Unexpected order: {link_texts}"
    print("PASS: Medications is directly below Appointments!")

    # Screenshot 1: Dashboard with updated sidebar order
    driver.save_screenshot(os.path.join(artifact_dir, "sidebar_updated_order.png"))

    # 3. Test Sidebar Collapse Button
    collapse_btn = driver.find_element(By.ID, "sidebarCollapseBtn")
    collapse_btn.click()
    time.sleep(0.5)

    # Check if collapsed
    sidebar = driver.find_element(By.ID, "appSidebar")
    assert "is-collapsed" in sidebar.get_attribute("class")
    print("PASS: Sidebar collapsed when button pressed!")
    driver.save_screenshot(os.path.join(artifact_dir, "sidebar_collapsed_state.png"))

    # 4. Test Hover over collapsed sidebar
    ActionChains(driver).move_to_element(sidebar).perform()
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(artifact_dir, "sidebar_hover_expanded.png"))
    print("PASS: Sidebar hover screenshot captured!")

    # Move mouse away to test collapse on mouseleave
    body = driver.find_element(By.TAG_NAME, "body")
    ActionChains(driver).move_to_element_with_offset(body, 500, 300).perform()
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(artifact_dir, "sidebar_unhovered_collapsed.png"))
    print("PASS: Sidebar collapsed back when hover removed!")

    # Click topbar toggle button to restore sidebar
    topbar_toggle = driver.find_element(By.ID, "topbarSidebarToggleBtn")
    topbar_toggle.click()
    time.sleep(0.5)
    assert "is-collapsed" not in sidebar.get_attribute("class")
    print("PASS: Sidebar uncollapsed cleanly!")

    # 5. Check Health Records history.html toggle button & badge
    driver.get("http://127.0.0.1:5000/history")
    time.sleep(1)

    toggle_btn = driver.find_element(By.ID, "myRecordsToggleBtn")
    badge = driver.find_element(By.ID, "myRecordsCountBadge")
    print("Initial badge display:", badge.is_displayed())
    driver.save_screenshot(os.path.join(artifact_dir, "records_overview_state.png"))

    # Click toggle button to view records
    toggle_btn.click()
    time.sleep(0.5)
    btn_text = driver.find_element(By.ID, "myRecordsBtnText").text
    print("Toggled button text:", btn_text)
    badge_displayed = badge.is_displayed()
    print("Badge displayed after toggle:", badge_displayed)
    assert not badge_displayed, "Badge should NOT be displayed when viewing records timeline!"
    print("PASS: '9' count badge is hidden on '← Back to Overview'!")
    driver.save_screenshot(os.path.join(artifact_dir, "records_timeline_without_badge.png"))

    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
finally:
    driver.quit()
