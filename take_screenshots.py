"""
Take 3 live screenshots of the StudyWiseAI app for the poster.
Screens:
  1. Home / landing page
  2. AI Chat modal
  3. Career Counseling tab
"""
import pathlib
import requests
from playwright.sync_api import sync_playwright

API = "http://127.0.0.1:8000"
FRONT = "http://localhost:5173"
USER = {"username": "poster_demo", "email": "poster@studywise.ai",
        "password": "Demo1234!", "full_name": "Demo User"}

out = pathlib.Path(r"c:/Code/StudyWiseAI/docs/screenshots")
out.mkdir(exist_ok=True)

# ── Pre-register the test user via API (idempotent) ─────────────────────────
try:
    r = requests.post(f"{API}/api/auth/register", json=USER, timeout=10)
    print("Register:", r.status_code, r.text[:120])
except Exception as e:
    print("Register error:", e)

# ── Playwright screenshots ───────────────────────────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 430, "height": 932},
                              device_scale_factor=2)   # iPhone 14 Plus, retina
    page = ctx.new_page()

    # ── Screen 1: Weekly Planner modal (calendar view) ──────────────────────
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(FRONT, wait_until="networkidle")
    page.wait_for_timeout(1500)
    nav_h = page.evaluate("() => document.querySelector('nav').offsetHeight")
    print(f"Nav height (1280px): {nav_h}px")
    page.click("button:has-text('Login')")
    page.wait_for_selector("input[name='username']", timeout=8000)
    page.fill("input[name='username']", USER["username"])
    page.fill("input[name='password']", USER["password"])
    page.click("button[type='submit']")
    page.wait_for_timeout(3000)
    print("Login submitted")
    page.click("button:has-text('Planner')", timeout=5000)
    page.wait_for_timeout(1500)
    page.click("button:has-text('Open Planner')", timeout=5000)
    page.wait_for_timeout(2000)
    # Full viewport with the modal open (dark overlay + calendar modal)
    page.screenshot(
        path=str(out / "screen1_home.png"),
        clip={"x": 0, "y": nav_h, "width": 1280, "height": 900 - nav_h},
    )
    print("Shot 1: weekly planner modal saved")
    # Switch back to 430px for screens 2 and 3
    page.set_viewport_size({"width": 430, "height": 932})
    page.goto(FRONT, wait_until="networkidle")
    page.wait_for_timeout(1500)
    try:
        login_btn = page.locator("button:has-text('Login')")
        if login_btn.is_visible():
            login_btn.click()
            page.wait_for_selector("input[name='username']", timeout=5000)
            page.fill("input[name='username']", USER["username"])
            page.fill("input[name='password']", USER["password"])
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)
            print("Re-logged in at 430px")
    except Exception as e:
        print("Re-login check:", e)

    # ── Screen 2: Chat modal (dark overlay) ─────────────────────────────────
    try:
        # Navigate to AI Assistant tab first
        page.click("button:has-text('AI Assistant')", timeout=5000)
        page.wait_for_timeout(1500)
        # Click Open Chat to launch the actual modal
        page.click("button:has-text('Open Chat')", timeout=5000)
        page.wait_for_timeout(2000)
        # Clip at nav height so the nav bar is excluded; dark overlay + modal card shown
        nav_h2 = page.evaluate("() => document.querySelector('nav').offsetHeight")
        page.screenshot(
            path=str(out / "screen2_chat.png"),
            clip={"x": 0, "y": nav_h2, "width": 430, "height": 932 - nav_h2},
        )
        print("Shot 2: chat modal saved")
    except Exception as e:
        print("Chat modal attempt:", e)
        nav_h2 = page.evaluate("() => document.querySelector('nav').offsetHeight")
        page.screenshot(
            path=str(out / "screen2_chat.png"),
            clip={"x": 0, "y": nav_h2, "width": 430, "height": 932 - nav_h2},
        )
        print("Shot 2 (fallback): AI Assistant saved")

    # ── Screen 3: Career Counseling (768px — renders correctly) ─────────────
    # Close the chat modal by clicking the × button (inside modal, not blocked)
    try:
        page.click("button:has-text('×')", timeout=3000)
        page.wait_for_timeout(1000)
        print("Chat modal closed via × button")
    except Exception as e:
        print("Modal close failed:", e)
        pass
    # Switch to 768px — career page is blank at 430px
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(FRONT, wait_until="networkidle")
    page.wait_for_timeout(1000)
    try:
        login_btn = page.locator("button:has-text('Login')")
        if login_btn.is_visible():
            login_btn.click()
            page.wait_for_selector("input[name='username']", timeout=5000)
            page.fill("input[name='username']", USER["username"])
            page.fill("input[name='password']", USER["password"])
            page.click("button[type='submit']")
            page.wait_for_timeout(2500)
    except Exception:
        pass
    page.click("button:has-text('Career Counseling')", timeout=6000)
    page.wait_for_timeout(2500)
    nav_h3 = page.evaluate("() => document.querySelector('nav').offsetHeight")
    page.screenshot(
        path=str(out / "screen3_career.png"),
        clip={"x": 0, "y": nav_h3, "width": 768, "height": 1024 - nav_h3},
    )
    print("Shot 3: career counseling saved")

    browser.close()

print("All screenshots saved to:", out)
