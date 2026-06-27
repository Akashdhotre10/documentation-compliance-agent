import json
import re


class JSONValidator:

    def validate(self, text):

        try:
            return json.loads(text)

        except Exception:
            pass

        try:
            match = re.search(r"\{[\s\S]*\}", text)

            if match:
                return json.loads(match.group())

        except Exception:
            pass

        return {
            "compliance_score": 0,
            "matched": [],
            "missing": [],
            "extra": [],
            "summary": "Invalid AI response"
        }