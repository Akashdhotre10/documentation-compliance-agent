from rapidfuzz import fuzz


class FuzzyMatcher:

    def __init__(self, threshold=65):
        self.threshold = threshold

    def _normalize(self, text):
        return (
            text.lower()
            .replace("faq", "faqs")
            .replace("facility", "facilities")
            .replace("application", "applications")
            .replace("user", "users")
            .strip()
        )

    def match(self, documentation, ui):

        matched = []
        missing = []

        # Remove duplicates
        documentation = list(dict.fromkeys(documentation))
        ui = list(dict.fromkeys(ui))

        normalized_ui = [self._normalize(i) for i in ui]

        for doc in documentation:

            doc = doc.strip()

            # Ignore long descriptive paragraphs
            if len(doc.split()) > 8:
                continue

            doc_norm = self._normalize(doc)

            best = 0

            for item in normalized_ui:

                score = max(
                    fuzz.ratio(doc_norm, item),
                    fuzz.partial_ratio(doc_norm, item),
                    fuzz.token_sort_ratio(doc_norm, item),
                )

                best = max(best, score)

            if best >= self.threshold:
                matched.append(doc)
            else:
                missing.append(doc)

        extra = []

        normalized_doc = [self._normalize(i) for i in documentation]

        for item in ui:

            item_norm = self._normalize(item)

            best = 0

            for doc in normalized_doc:

                score = max(
                    fuzz.ratio(item_norm, doc),
                    fuzz.partial_ratio(item_norm, doc),
                    fuzz.token_sort_ratio(item_norm, doc),
                )

                best = max(best, score)

            if best < self.threshold:
                extra.append(item)

        return matched, missing, extra