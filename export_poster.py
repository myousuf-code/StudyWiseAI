"""Export poster_chart.html to PDF and PNG."""
import pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(r"c:/Code/StudyWiseAI/docs/poster_chart.html").resolve()
out_pdf = html.parent / "StudyWiseAI_Poster_A0_v9.pdf"
out_png = html.parent / "StudyWiseAI_Poster_v9.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 3200, "height": 4600})
    page.goto(html.as_uri(), wait_until="networkidle")
    page.wait_for_timeout(2000)

    page.pdf(
        path=str(out_pdf),
        width="841mm",
        height="1189mm",
        print_background=True,
    )
    print("PDF saved:", out_pdf)

    page.screenshot(
        path=str(out_png),
        full_page=True,
    )
    print("PNG saved:", out_png)

    browser.close()
