class ScoreCalculator:

    def calculate(
        self,
        matched=None,
        missing=None,
        extra=None,
        component_results=None
    ):

        matched = matched or []
        missing = missing or []
        extra = extra or []

        matched_count = len(matched)
        missing_count = len(missing)
        extra_count = len(extra)

        expected = matched_count + missing_count

        if expected == 0:
            return 100

        score = (matched_count / expected) * 100

        # Small penalty for unexpected UI
        score -= min(extra_count * 1.5, 10)

        score = max(0, min(100, round(score)))

        print("\n========== SCORE ==========")
        print("Matched :", matched_count)
        print("Missing :", missing_count)
        print("Extra   :", extra_count)
        print("Score   :", score)
        print("===========================\n")

        return score