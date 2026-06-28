from rapidfuzz import fuzz


class ComponentMatcher:
    """
    Compare documentation components with UI components using
    synonym mapping and fuzzy matching.
    """

    def __init__(self, threshold=80):

        self.threshold = threshold

        # Known equivalent terms
        self.synonyms = {
            "facility": "facilities",
            "application": "applications",
            "faq": "faqs",
            "user": "users",
            "role": "user role",
            "status chip": "status",
            "waiver type": "application type"
        }

    # -----------------------------------------

    def normalize(self, text):

        text = str(text).strip().lower()

        if text in self.synonyms:
            return self.synonyms[text]

        return text

    # -----------------------------------------

    def compare(self, expected, actual):

        matched = []
        missing = []
        extra = []

        expected = expected or []
        actual = actual or []

        matched_actual = set()

        # -----------------------------
        # Compare expected -> actual
        # -----------------------------

        for exp in expected:

            exp_norm = self.normalize(exp)

            best_score = 0
            best_actual = None

            for act in actual:

                act_norm = self.normalize(act)

                score = fuzz.token_sort_ratio(
                    exp_norm,
                    act_norm
                )

                if score > best_score:
                    best_score = score
                    best_actual = act

            if best_score >= self.threshold:
                matched.append(exp)
                matched_actual.add(best_actual)
            else:
                missing.append(exp)

        # -----------------------------
        # Find extra UI elements
        # -----------------------------

        for act in actual:

            if act not in matched_actual:
                extra.append(act)

        return matched, missing, extra