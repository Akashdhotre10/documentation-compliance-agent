from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self, headless=False):
        self.headless = headless

    def launch(self):

        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=self.headless
        )

        page = browser.new_page()

        return playwright, browser, page