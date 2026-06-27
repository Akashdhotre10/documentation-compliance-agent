from app.extractor.browser import BrowserManager
from app.extractor.login import Login
from app.extractor.screenshot import ScreenshotManager
from app.extractor.dom_parser import DOMParser

from app.parser.json_writer import JSONWriter


browser = BrowserManager(False)

playwright, chrome, page = browser.launch()

Login(page).login()

ScreenshotManager(page).capture("dashboard")

elements = DOMParser(page).extract()

JSONWriter.save(
    elements,
    "data/extracted/dashboard.json"
)

chrome.close()

playwright.stop()