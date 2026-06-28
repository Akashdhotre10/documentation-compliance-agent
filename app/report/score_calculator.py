class ScoreCalculator:

    # Per-component weights to reflect relative importance in scoring.
    DEFAULT_WEIGHTS = {
        "headings": 0.5,
        "buttons": 1.0,
        "forms": 1.5,
        "table_headers": 1.0,
        "cards": 0.8,
        "badges": 0.4,
        "tabs": 0.6
    }

    def calculate(
        self,
        matched=None,
        missing=None,
        extra=None,
        component_results=None
    ):

        # Safety check
        if not component_results:
            return 0

        total_weight = 0.0
        weighted_score = 0.0
        total_expected = 0
        total_matched = 0
        total_extra = 0

        # Compute per-component coverage and aggregate with weights
        for component, result in component_results.items():
            matched_count = len(result.get("matched", []))
            missing_count = len(result.get("missing", []))
            extra_count = len(result.get("extra", []))

            expected = matched_count + missing_count
            total_expected += expected
            total_matched += matched_count
            total_extra += extra_count

            weight = self.DEFAULT_WEIGHTS.get(component, 1.0)
            total_weight += weight

            # If nothing expected for this component, treat coverage as perfect
            if expected == 0:
                comp_coverage = 1.0
            else:
                comp_coverage = matched_count / expected

            weighted_score += comp_coverage * weight

        # If there are no weighted components, default to full score
        if total_weight == 0:
            base_score = 100.0
        else:
            base_score = (weighted_score / total_weight) * 100.0

        # Apply a modest penalty for extra/unexpected UI elements.
        # Penalty scales with the ratio of extras to expected items and is capped.
        if total_expected == 0:
            penalty = 0.0
        else:
            extra_ratio = total_extra / total_expected
            penalty = min(extra_ratio * 100.0 * 0.10, 15.0)  # up to 15% penalty

        final_score = base_score - penalty
        final_score = max(0, min(100, round(final_score)))

        # Debug output
        print("\n========== COVERAGE WEIGHTED SCORE ==========")
        print("Total Matched :", total_matched)
        print("Total Expected :", total_expected)
        print("Total Extra :", total_extra)
        print("Base Score (weighted) :", round(base_score, 2))
        print("Penalty :", round(penalty, 2))
        print("Final Score :", final_score)
        print("============================================")

        return final_score