from rapidfuzz import fuzz


class SemanticMatcher:

    def __init__(self, pages):
        self.pages = pages

    def find_best_match(self, ui_title):

        ui = ui_title.lower().strip()

        # ---------- STEP 1 ----------
        # Direct keyword match in documentation title

        for page in self.pages:

            title = page["title"].lower()

            if ui in title:
                return page, 100

        # ---------- STEP 2 ----------
        # Keyword match in documentation content

        for page in self.pages:

            content = page["content"].lower()

            if ui in content:
                return page, 95

        # ---------- STEP 3 ----------
        # Fuzzy title matching

        best_page = None
        best_score = 0

        for page in self.pages:

            score = fuzz.token_set_ratio(
                ui,
                page["title"].lower()
            )

            if score > best_score:
                best_score = score
                best_page = page

        return best_page, best_score