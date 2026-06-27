import json
import glob


class DashboardSummary:

    def overall_score(self):

        scores = []

        for file in glob.glob("reports/*.json"):

            try:

                with open(file, encoding="utf-8") as f:

                    result = json.load(f)

                scores.append(
                    result["compliance_score"]
                )

            except:
                pass

        if len(scores) == 0:

            return 0

        return round(sum(scores) / len(scores), 1)