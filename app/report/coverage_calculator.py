class CoverageCalculator:

    def calculate(self, component_results):

        coverage = {}

        overall_expected = 0
        overall_matched = 0

        for component, result in component_results.items():

            matched = len(result["matched"])
            missing = len(result["missing"])

            expected = matched + missing

            if expected == 0:
                percent = 100
            else:
                percent = round((matched / expected) * 100)

            coverage[component] = {
                "matched": matched,
                "expected": expected,
                "coverage": percent
            }

            overall_expected += expected
            overall_matched += matched

        if overall_expected == 0:
            overall = 100
        else:
            overall = round(
                overall_matched / overall_expected * 100
            )

        return coverage, overall