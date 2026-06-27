from app.extractor.browser import BrowserManager
from app.extractor.login import Login
from app.extractor.crawler import WebsiteCrawler
from app.extractor.ui_extractor import UIExtractor

browser = BrowserManager(headless=False)

playwright, chrome, page = browser.launch()

Login(page).login()

crawler = WebsiteCrawler(page)

extractor = UIExtractor(page)

for page_name in crawler.NAVIGATION:

    success = crawler.visit(page_name)

    if not success:

        print(f"Skipping {page_name}")

        continue

    data = extractor.extract()

    filename = page_name.lower().replace(" ", "_")

    extractor.save(filename, data)

    print(f"Saved {filename}.json")

print("Website Crawling Completed")

chrome.close()

playwright.stop()