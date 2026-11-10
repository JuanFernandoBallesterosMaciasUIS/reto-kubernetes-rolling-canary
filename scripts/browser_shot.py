# Toma pantallazo real del navegador (Microsoft Edge headless) a la app expuesta por el Service.
import sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": 1100, "height": 500})
    pg.goto(url)
    pg.screenshot(path=out)
    b.close()
