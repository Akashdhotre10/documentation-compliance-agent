import json
import os
import re


class UIExtractor:
    """
    Extract visible UI components from the current page.
    The output is optimized for AI compliance comparison.
    """

    def __init__(self, page):
        self.page = page

    # -------------------------------------------------

    def clean_text(self, text):

        if not text:
            return ""

        text = text.strip()

        # collapse spaces
        text = re.sub(r"\s+", " ", text)

        return text

    # -------------------------------------------------

    def valid_text(self, text):
        """
        Decide whether extracted text is meaningful for
        documentation comparison.
        """

        text = self.clean_text(text)

        if not text:
            return False

        # Ignore only pure numbers
        if text.isdigit():
            return False

        # Ignore very short text
        if len(text) <= 2:
            return False

        # Ignore common UI noise
        ignore = {
            "...",
            "|",
            "-",
            "--",
            ">>",
            "<<",
            ">",
            "<"
        }

        if text in ignore:
            return False

        return True

    # -------------------------------------------------

    def extract(self):

        # Give React time to finish rendering
        self.page.wait_for_timeout(1500)

        data = {}
        data["url"] = self.page.url

        # =====================================================
        # PAGE TITLE
        # =====================================================

        title = ""

        try:
            h1 = self.page.locator("h1")
            if h1.count() > 0:
                title = self.clean_text(h1.first.inner_text())
        except Exception:
            pass

        if not title:
            try:
                title = self.page.title()
            except Exception:
                title = ""

        data["title"] = title

        print("\nDetected Title :", title)
        print("Current URL    :", self.page.url)

        # =====================================================
        # HEADINGS
        # =====================================================

        headings = []

        try:
            locator = self.page.locator("h1,h2,h3")
            for i in range(locator.count()):
                text = self.clean_text(locator.nth(i).inner_text())
                if self.valid_text(text) and text not in headings:
                    headings.append(text)
        except Exception:
            pass

        data["headings"] = headings

        # =====================================================
        # BUTTONS
        # =====================================================

        buttons = []

        try:
            locator = self.page.locator(
                "button, "
                "input[type='button'], "
                "input[type='submit'], "
                "[role='button']"
            )
            ignore = {
                "Dashboard",
                "Home",
                "Logout",
                "Profile"
            }

            for i in range(locator.count()):
                element = locator.nth(i)
                text = ""
                try:
                    text = element.inner_text()
                except Exception:
                    pass
                if not text:
                    text = element.get_attribute("value")
                if not text:
                    text = element.get_attribute("aria-label")
                text = self.clean_text(text or "")
                if not self.valid_text(text):
                    continue
                if text in ignore:
                    continue
                if text not in buttons:
                    buttons.append(text)
        except Exception:
            pass

        data["buttons"] = sorted(buttons)

        # =====================================================
        # SEARCH BOXES
        # =====================================================

        search = []

        try:
            locator = self.page.locator("input")
            for i in range(locator.count()):
                placeholder = locator.nth(i).get_attribute("placeholder")
                placeholder = self.clean_text(placeholder or "")
                if placeholder and placeholder not in search:
                    search.append(placeholder)
        except Exception:
            pass

        data["search_boxes"] = search

        # =====================================================
        # TABLE HEADERS
        # =====================================================

        headers = []

        try:
            locator = self.page.locator("th, [role='columnheader'], caption")
            for i in range(locator.count()):
                element = locator.nth(i)
                text = ""
                try:
                    text = element.inner_text()
                except Exception:
                    pass
                if not text:
                    text = element.get_attribute("aria-label")
                text = self.clean_text(text or "")
                if self.valid_text(text) and text not in headers:
                    headers.append(text)
        except Exception:
            pass

        data["table_headers"] = sorted(headers)

        # =====================================================
        # FORMS
        # =====================================================

        forms = []

        try:
            locator = self.page.locator("input, textarea, select, label")
            for i in range(locator.count()):
                element = locator.nth(i)
                value = ""
                try:
                    value = element.inner_text()
                except Exception:
                    pass
                if not value:
                    value = element.get_attribute("placeholder")
                if not value:
                    value = element.get_attribute("aria-label")
                if not value:
                    value = element.get_attribute("name")
                if not value:
                    value = element.get_attribute("id")
                value = self.clean_text(value or "")
                if self.valid_text(value) and value not in forms:
                    forms.append(value)
        except Exception:
            pass

        data["forms"] = sorted(forms)

        # =====================================================
        # TABLES PRESENT?
        # =====================================================

        try:
            data["tables"] = self.page.locator("table").count()
        except Exception:
            data["tables"] = 0

        # =====================================================
        # CARDS
        # =====================================================

        cards = []

        try:
            card_selector = ",".join([
                ".card",
                ".dashboard-card",
                ".MuiCard-root",
                ".ant-card",
                ".panel",
                "article",
                "[class*='card']"
            ])

            locator = self.page.locator(card_selector)

            for i in range(locator.count()):
                element = locator.nth(i)
                text = ""
                try:
                    text = element.inner_text()
                except Exception:
                    pass

                text = self.clean_text(text)

                if self.valid_text(text):
                    text = text.split("\n")[0]
                    if text not in cards:
                        cards.append(text)

        except Exception:
            pass

        data["cards"] = sorted(cards)

        # =====================================================
        # BADGES
        # =====================================================

        badges = []

        try:
            locator = self.page.locator(".badge, .chip, .status, .tag")
            for i in range(locator.count()):
                text = self.clean_text(locator.nth(i).inner_text())
                if self.valid_text(text) and text not in badges:
                    badges.append(text)
        except Exception:
            pass

        data["badges"] = sorted(badges)

        # =====================================================
        # TABS
        # =====================================================

        tabs = []

        try:
            locator = self.page.locator("[role='tab'], .tab")
            for i in range(locator.count()):
                text = self.clean_text(locator.nth(i).inner_text())
                if self.valid_text(text) and text not in tabs:
                    tabs.append(text)
        except Exception:
            pass

        data["tabs"] = sorted(tabs)

        # =====================================================
        # CHARTS PRESENT?
        # =====================================================

        try:
            chart_selector = ",".join([
                ".recharts-wrapper",
                ".apexcharts-canvas",
                ".highcharts-container",
                ".echarts-for-react",
                ".chart-container",
                "canvas.chartjs-render-monitor"
            ])

            charts = self.page.locator(chart_selector).count()
            data["charts"] = charts
        except Exception:
            data["charts"] = 0

        try:
            charts = self.page.locator("canvas,svg,.recharts-wrapper").count()
            data["charts"] = charts
        except Exception:
            data["charts"] = 0

        # =====================================================
        # DEBUG
        # =====================================================

        print("\n----------- UI SUMMARY -----------")
        print("Title :", data["title"])
        print("Headings :", len(data["headings"]))
        print("Buttons :", len(data["buttons"]))
        print("Search Boxes :", len(data["search_boxes"]))
        print("Table Headers :", len(data["table_headers"]))
        print("Forms :", len(data["forms"]))
        print("Cards :", len(data["cards"]))
        print("Badges :", len(data["badges"]))
        print("Tabs :", len(data["tabs"]))
        print("Tables :", data["tables"])
        print("Charts :", data["charts"])
        print("----------------------------------")

        return data

    # -------------------------------------------------

    def save(self, filename, data):

        os.makedirs("data/extracted", exist_ok=True)

        filepath = os.path.join(
            "data",
            "extracted",
            f"{filename}.json"
        )

        with open(filepath, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"\nSaved : {filepath}")


    # -------------------------------------------------

    def save_screenshot(self, filename):

        os.makedirs("screenshots", exist_ok=True)

        filepath = os.path.join(
            "screenshots",
            f"{filename}.png"
        )

        self.page.screenshot(
            path=filepath,
            full_page=True
        )

        print(f"Screenshot saved : {filepath}")

        return filepath