from dotenv import load_dotenv
import os

load_dotenv()


class Login:
    def __init__(self, page):
        self.page = page
        self.base_url = os.getenv("BASE_URL")
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")

    def login(self):

        # Open Landing Page
        self.page.goto(self.base_url)

        # Wait until page loads
        self.page.wait_for_load_state("domcontentloaded")

        print("Opened Landing Page")

        # Click Getting Started
        self.page.locator("text=Getting Started").click()

        # Wait for Login Page
        self.page.wait_for_selector('input[type="email"]')

        print("Login Page Loaded")

        # Fill Email
        self.page.fill('input[type="email"]', self.email)

        # Fill Password
        self.page.fill('input[type="password"]', self.password)

        print("Credentials Entered")

        # Click Login
        self.page.locator("button:has-text('Login')").click()

        # Wait 5 seconds so React can finish redirecting
        self.page.wait_for_timeout(5000)

        print("Current URL:", self.page.url)

        # Save a debug screenshot
        self.page.screenshot(
            path="data/screenshots/login_debug.png",
            full_page=True
        )

        print("Screenshot saved.")

        print("Login Finished")