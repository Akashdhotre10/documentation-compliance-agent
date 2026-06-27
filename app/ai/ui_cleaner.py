class UICleaner:
    """
    Removes global navigation and unnecessary
    UI elements before sending data to the AI.
    """

    def clean(self, ui):

        cleaned = {}

        cleaned["title"] = ui.get("title", "")

        cleaned["headings"] = ui.get("headings", [])

        cleaned["buttons"] = ui.get("buttons", [])

        cleaned["table_headers"] = ui.get("table_headers", [])

        cleaned["search_boxes"] = ui.get("search_boxes", [])

        # Ignore these because they appear on every page
        # and are not page-specific.
        # sidebar, links, url are intentionally excluded.

        return cleaned