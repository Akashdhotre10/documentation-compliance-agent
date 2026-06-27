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

                title = self.clean_text(
                    h1.first.inner_text()
                )

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

                text = self.clean_text(
                    locator.nth(i).inner_text()
                )

                if self.valid_text(text):

                    if text not in headings:

                        headings.append(text)

        except Exception:
            pass

        data["headings"] = headings

        # =====================================================
        # BUTTONS
        # =====================================================

        buttons = []

        try:

            locator = self.page.locator("button")

            for i in range(locator.count()):

                text = self.clean_text(
                    locator.nth(i).inner_text()
                )

                if not self.valid_text(text):
                    continue

                # Ignore navigation buttons

                ignore = [

                    "Dashboard",
                    "Home",
                    "Logout",
                    "Profile"

                ]

                if text in ignore:
                    continue

                if text not in buttons:
                    buttons.append(text)

        except Exception:
            pass

        data["buttons"] = buttons

        # =====================================================
        # SEARCH BOXES
        # =====================================================

        search = []

        try:

            locator = self.page.locator("input")

            for i in range(locator.count()):

                placeholder = locator.nth(i).get_attribute(
                    "placeholder"
                )

                placeholder = self.clean_text(
                    placeholder or ""
                )

                if placeholder:

                    if placeholder not in search:

                        search.append(placeholder)

        except Exception:
            pass

        data["search_boxes"] = search

        # =====================================================
        # TABLE HEADERS
        # =====================================================

        headers = []

        try:

            locator = self.page.locator("th")

            for i in range(locator.count()):

                text = self.clean_text(
                    locator.nth(i).inner_text()
                )

                if self.valid_text(text):

                    if text not in headers:

                        headers.append(text)

        except Exception:
            pass

        data["table_headers"] = headers

        # =====================================================
        # FORMS
        # =====================================================

        forms = []

        try:

            locator = self.page.locator(
                "label,input,textarea,select"
            )

            for i in range(locator.count()):

                item = locator.nth(i)

                text = ""

                try:
                    text = item.inner_text()
                except:
                    pass

                if not text:
                    text = item.get_attribute("placeholder")

                if not text:
                    text = item.get_attribute("name")

                text = self.clean_text(text or "")

                if self.valid_text(text):

                    if text not in forms:

                        forms.append(text)

        except Exception:
            pass

        data["forms"] = forms

        # =====================================================
        # TABLES PRESENT?
        # =====================================================

        try:

            data["tables"] = self.page.locator("table").count()

        except Exception:

            data["tables"] = 0

        # =====================================================
        # CHARTS PRESENT?
        # =====================================================

        try:

            charts = self.page.locator(
                "canvas,svg,.recharts-wrapper"
            ).count()

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
        print("Search :", len(data["search_boxes"]))
        print("Table Headers :", len(data["table_headers"]))
        print("Forms :", len(data["forms"]))
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