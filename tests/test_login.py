from app.extractor.browser import BrowserManager
from app.extractor.login import Login

browser = BrowserManager(headless=False)

playwright, chrome, page = browser.launch()

login = Login(page)

login.login()

input("\nPress ENTER to close browser...")

chrome.close()

playwright.stop()