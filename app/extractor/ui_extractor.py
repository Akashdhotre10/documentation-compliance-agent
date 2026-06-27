import json
import os


class UIExtractor:
    """
    Extracts structured UI information from a page
    and saves it as JSON.
    """

    def __init__(self, page):
        self.page = page

    def extract(self):

        data = {}

      
        data["url"] = self.page.url


        try:
            data["title"] = (
                self.page.locator("h1")
                .first
                .inner_text()
                .strip()
            )
        except Exception:
            data["title"] = ""

        headings = []

        try:
            for heading in self.page.locator("h1, h2, h3").all():

                text = heading.inner_text().strip()

                if text:
                    headings.append(text)

        except Exception:
            pass

        data["headings"] = sorted(set(headings))

      
        buttons = []

        try:

            for button in self.page.locator("button").all():

                text = button.inner_text().strip()

                if not text:
                    continue

                # Ignore pure numbers
                if text.isdigit():
                    continue

                # Ignore initials like AD
                if len(text) <= 2 and text.isupper():
                    continue

                buttons.append(text)

        except Exception:
            pass

        data["buttons"] = sorted(set(buttons))

       
        sidebar = []

        try:

            nav_items = self.page.locator("[data-testid^='nav-']").all()

            for item in nav_items:

                text = item.inner_text().strip()

                if text:
                    sidebar.append(text)

        except Exception:
            pass

        data["sidebar"] = sidebar

     
        search_boxes = []

        try:

            for inp in self.page.locator("input").all():

                placeholder = inp.get_attribute("placeholder")

                if placeholder:
                    search_boxes.append(placeholder)

        except Exception:
            pass

        data["search_boxes"] = sorted(set(search_boxes))

      
        table_headers = []

        try:

            for th in self.page.locator("th").all():

                text = th.inner_text().strip()

                if text:
                    table_headers.append(text)

        except Exception:
            pass

        data["table_headers"] = table_headers

      
        links = []

        try:

            for link in self.page.locator("a").all():

                text = link.inner_text().strip()

                if text:
                    links.append(text)

        except Exception:
            pass

        data["links"] = sorted(set(links))

        return data



    def save(self, filename, data):

        os.makedirs("data/extracted", exist_ok=True)

        filepath = os.path.join(
            "data",
            "extracted",
            f"{filename}.json"
        )

        with open(filepath, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f" Saved: {filepath}")