import json

from app.matcher.semantic_matcher import SemanticMatcher


class PageMatcher:

    def __init__(self):

        with open(
            "data/extracted/guidelines.json",
            encoding="utf-8"
        ) as file:

            self.guidelines = json.load(file)

        self.semantic = SemanticMatcher(
            self.guidelines
        )

    def get_page(self, page_title):

        page, score = self.semantic.find_best_match(
            page_title
        )

        print("\n---------------------------")
        print("Semantic Page Match")
        print("---------------------------")
        print("Website Page :", page_title)
        print("Matched Doc  :", page["title"])
        print("Confidence   :", score)
        print("---------------------------\n")

        if page is not None:
            return page
        return None