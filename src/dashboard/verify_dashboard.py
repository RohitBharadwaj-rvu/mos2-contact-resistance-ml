"""
Dashboard Verification Script using Playwright (Sprint 6.b.3).
Spawns the local Flask dashboard, verifies HTTP 200 OK and UI rendering,
and captures a live screenshot adhering to user verification guidelines.
"""

import os
import sys
import time
import urllib.request
import subprocess
from pathlib import Path

ARTIFACT_DIR = Path(r"C:\Users\rohit\.gemini\antigravity\brain\40351c3a-3e08-415f-8617-d9dac2b5ded1")
ARTIFACT_SCREENSHOT = ARTIFACT_DIR / "dashboard_live_verification.png"
REPORT_SCREENSHOT = Path(__file__).resolve().parents[2] / "reports" / "figures" / "dashboard_live_screenshot.png"
DASHBOARD_URL = "http://127.0.0.1:5050"


def wait_for_server(url: str, timeout: int = 15) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def verify_and_capture_screenshot():
    print(f"Launching dashboard on {DASHBOARD_URL}...")
    server_process = subprocess.Popen([sys.executable, "-m", "src.dashboard.app"])
    
    try:
        if not wait_for_server(DASHBOARD_URL, timeout=15):
            raise RuntimeError(f"Dashboard failed to start on {DASHBOARD_URL} within 15 seconds.")
        print("Dashboard is live and responding with HTTP 200 OK.")

        # Playwright capture
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(DASHBOARD_URL)
            page.wait_for_selector("#predict-form")
            # Wait for JS initial prediction calculation
            page.wait_for_timeout(1500)

            ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
            REPORT_SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)

            page.screenshot(path=str(ARTIFACT_SCREENSHOT), full_page=True)
            page.screenshot(path=str(REPORT_SCREENSHOT), full_page=True)
            print(f"Screenshot successfully captured to: {ARTIFACT_SCREENSHOT}")
            print(f"Report screenshot saved to: {REPORT_SCREENSHOT}")
            browser.close()
            
    finally:
        server_process.terminate()
        server_process.wait()
        print("Server process shut down cleanly.")


if __name__ == "__main__":
    verify_and_capture_screenshot()
