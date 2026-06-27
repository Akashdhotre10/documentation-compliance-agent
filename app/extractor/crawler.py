from playwright.sync_api import TimeoutError


class WebsiteCrawler:

    NAVIGATION = {
        "My Applications": "nav-my-applications",
        "Facilities": "nav-facilities",
        "Action Items": "nav-action-items",
        "User Management": "nav-user-management",
        "Announcements": "nav-announcements",
        "Settings": "nav-settings",
        "FAQs": "nav-faqs",
        "Tickets": "nav-tickets",
        "Contact": "nav-contact",
    }

    def __init__(self, page):
        self.page = page

    def visit(self, page_name):

        print(f"\nOpening {page_name}")

        try:

            self.page.get_by_test_id(
                self.NAVIGATION[page_name]
            ).click()

            self.page.wait_for_load_state("networkidle")

            print("[OK] Opened")

            print("Current URL:", self.page.url)

            return True

        except TimeoutError:

            print(f"[Failed] to open {page_name}")

            return False