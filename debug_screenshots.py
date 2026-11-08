"""Retake screen3 at 768px with scroll to show content"""
from playwright.sync_api import sync_playwright

FRONT = "http://localhost:5173"
USER = {"username": "poster_demo", "password": "Demo1234!"}

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 768, "height": 1024},
                              device_scale_factor=2)
    page = ctx.new_page()
    page.goto(FRONT, wait_until="networkidle")
    page.wait_for_timeout(1000)

    # login
    page.click("button:has-text('Login')")
    page.wait_for_selector("input[name='username']", timeout=6000)
    page.fill("input[name='username']", USER["username"])
    page.fill("input[name='password']", USER["password"])
    page.click("button[type='submit']")
    page.wait_for_timeout(2500)
    print("Logged in")

    # click career tab
    page.click("button:has-text('Career Counseling')", timeout=5000)
    page.wait_for_timeout(2000)

    # Clip below the nav bar
    nav_h = page.evaluate("() => document.querySelector('nav').offsetHeight")
    print(f"Nav height (768px): {nav_h}px")
    page.screenshot(
        path="docs/screenshots/screen3_career.png",
        clip={"x": 0, "y": nav_h, "width": 768, "height": 1024 - nav_h},
    )
    print("screen3 saved")
    browser.close()
