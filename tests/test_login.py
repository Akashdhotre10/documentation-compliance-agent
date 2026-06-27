from app.extractor.browser import BrowserManager
from app.extractor.login import Login

browser = BrowserManager(headless=False)

playwright, chrome, page = browser.launch()

Login(page).login()

chrome.close()

playwright.stop()