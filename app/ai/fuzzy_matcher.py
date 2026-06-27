from rapidfuzz import fuzz


class FuzzyMatcher:

    def __init__(self, threshold=75):

        self.threshold = threshold

    def match(self, documentation, ui):

        matched = []
        missing = []

        for doc in documentation:

            found = False

            for item in ui:

                score = fuzz.token_sort_ratio(
                    doc.lower(),
                    item.lower()
                )

                if score >= self.threshold:

                    matched.append(doc)
                    found = True
                    break

            if not found:

                missing.append(doc)

        extra = []

        for item in ui:

            found = False

            for doc in documentation:

                score = fuzz.token_sort_ratio(
                    doc.lower(),
                    item.lower()
                )

                if score >= self.threshold:

                    found = True
                    break

            if not found:

                extra.append(item)

        return matched, missing, extra