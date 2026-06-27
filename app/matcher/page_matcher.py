import json


class PageMatcher:

    def __init__(self):

        with open(
            "data/extracted/guidelines.json",
            encoding="utf-8"
        ) as file:

            self.guidelines = json.load(file)

    def get_page(self, page_title):

        page_title = page_title.lower().strip()

        # ---------- Direct Match ----------
        for page in self.guidelines:

            title = page["title"].lower()

            if page_title == title:
                return page

            if page_title in title:
                return page

        # ---------- Support Pages ----------
        if page_title in ["faqs", "tickets", "contact"]:

            for page in self.guidelines:

                title = page["title"].lower()

                if "support" in title:
                    return page

        # ---------- User Management ----------
        if page_title == "user management":

            for page in self.guidelines:

                if "user management" in page["title"].lower():
                    return page

        # ---------- Action Items ----------
        if page_title == "action items":

            for page in self.guidelines:

                if "action items" in page["title"].lower():
                    return page

        # ---------- Announcements ----------
        if page_title == "announcements":

            for page in self.guidelines:

                if "announcements" in page["title"].lower():
                    return page

        # ---------- Settings ----------
        if page_title == "settings":

            for page in self.guidelines:

                if "settings" in page["title"].lower():
                    return page

        return None