from rapidfuzz import fuzz


class RuleMatcher:

    def __init__(self, threshold=85):
        self.threshold = threshold

    def normalize(self, text):
        if not text:
            return ""

        return (
            str(text)
            .lower()
            .replace("+", "")
            .replace("\n", " ")
            .replace("-", " ")
            .strip()
        )

    def compare_list(self, documentation, website):

        matched = []
        missing = []
        extra = []

        documentation = documentation or []
        website = website or []

        used = set()

        for doc in documentation:

            found = False

            for i, ui in enumerate(website):

                if i in used:
                    continue

                score = fuzz.token_sort_ratio(
                    self.normalize(doc),
                    self.normalize(ui)
                )

                if score >= self.threshold:

                    matched.append(doc)

                    used.add(i)

                    found = True

                    break

            if not found:

                missing.append(doc)

        for i, ui in enumerate(website):

            if i not in used:

                extra.append(ui)

        return matched, missing, extra