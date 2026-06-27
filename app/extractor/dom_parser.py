class DOMParser:

    def __init__(self, page):

        self.page = page

    def extract(self):

        elements = []

        buttons = self.page.query_selector_all("button")

        for button in buttons:

            try:

                elements.append({

                    "type": "button",

                    "text": button.inner_text()

                })

            except:

                pass

        links = self.page.query_selector_all("a")

        for link in links:

            try:

                elements.append({

                    "type": "link",

                    "text": link.inner_text()

                })

            except:

                pass

        headings = self.page.query_selector_all("h1,h2,h3")

        for heading in headings:

            try:

                elements.append({

                    "type": "heading",

                    "text": heading.inner_text()

                })

            except:

                pass

        return elements