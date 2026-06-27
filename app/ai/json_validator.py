import json
import re


class JSONValidator:
    """
    Validates and repairs AI responses.

    Ensures that the returned JSON always contains the
    required fields so the rest of the application
    never crashes due to malformed AI output.
    """

    DEFAULT_RESPONSE = {
        "compliance_score": 0,
        "matched": [],
        "missing": [],
        "extra": [],
        "issues": [],
        "summary": "Invalid AI response"
    }

    def validate(self, text):
        """
        Parse AI response and return a safe dictionary.
        """

        data = self._parse_json(text)

        if not isinstance(data, dict):
            return self.DEFAULT_RESPONSE.copy()

        # ---------- Required Fields ----------

        data.setdefault("compliance_score", 0)
        data.setdefault("matched", [])
        data.setdefault("missing", [])
        data.setdefault("extra", [])
        data.setdefault("issues", [])
        data.setdefault("summary", "")

        # ---------- Validate Types ----------

        if not isinstance(data["matched"], list):
            data["matched"] = []

        if not isinstance(data["missing"], list):
            data["missing"] = []

        if not isinstance(data["extra"], list):
            data["extra"] = []

        if not isinstance(data["issues"], list):
            data["issues"] = []

        if not isinstance(data["summary"], str):
            data["summary"] = ""

        if not isinstance(data["compliance_score"], (int, float)):
            data["compliance_score"] = 0

        return data

    def _parse_json(self, text):
        """
        Try parsing the AI response.

        First attempt:
            Direct JSON parsing.

        Second attempt:
            Extract JSON using regex.
        """

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

        return None