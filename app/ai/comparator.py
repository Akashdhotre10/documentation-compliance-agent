
import json

from numpy.strings import lower
from sqlalchemy import values

from app.ai.ignore_list import IGNORE
from app.matcher.page_matcher import PageMatcher
from app.ai.groq_client import GroqClient
from app.ai.ui_cleaner import UICleaner
from app.ai.prompt_builder import PromptBuilder
from app.ai.json_validator import JSONValidator
from app.ai.fuzzy_matcher import FuzzyMatcher
from app.ai.component_matcher import ComponentMatcher
from app.ai.section_extractor import SectionExtractor
from app.report.score_calculator import ScoreCalculator




class Comparator:

    def __init__(self):

        # Documentation matcher
        self.matcher = PageMatcher()

        self.section = SectionExtractor()

        # RapidFuzz matcher
        self.matcher_ai = FuzzyMatcher()

        self.component_matcher = ComponentMatcher()

        # AI
        self.ai = GroqClient()

        self.cleaner = UICleaner()

        self.prompt = PromptBuilder()

        self.validator = JSONValidator()

        self.score_calculator = ScoreCalculator()
        

        

    def compare_page(self, json_path):

        # --------------------------
        # Load UI JSON
        # --------------------------

        with open(json_path, encoding="utf-8") as file:
            ui = json.load(file)

        # --------------------------
        # Find matching documentation
        # --------------------------

        documentation = self.matcher.get_page(
            ui["title"]
        )

        documentation.setdefault("headings", [])
        documentation.setdefault("table_headers", [])

        print("\nSEMANTIC MATCH")
        print("Website Page :", ui["title"])

        if documentation is None:
            print("Documentation : None")

            return {
                "compliance_score": 0,
                "matched": [],
                "missing": [],
                "extra": [],
                "summary": f"No documentation found for page '{ui['title']}'"
            }

        print("Documentation :", documentation["title"])

        # --------------------------
        # Clean UI
        # --------------------------

        cleaned = self.cleaner.clean(ui)

        print("\nCLEANED UI\n")

        

        print(json.dumps(cleaned, indent=4))

        # --------------------------
        # Prepare lists for fuzzy matching
        # --------------------------

        documentation_items = [documentation["title"]]

        IGNORE = [
            "page lets",
            "page allows",
            "page enables",
            "page displays",
            "the following",
            "overview",
        ]

        for line in documentation["content"].split("\n"):

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            # Skip descriptive sentences
            if any(word in lower for word in IGNORE):
                continue

    # Skip very long paragraphs
            if len(line.split()) > 8:
                continue

            documentation_items.append(line)

# Remove duplicates
        documentation_items = list(dict.fromkeys(documentation_items))

# Add structured documentation fields
        for key in [
            "buttons",
            "forms",
            "headings",
            "table_headers",
            "cards",
            "badges",
            "tabs",
        ]:
            values = documentation.get(key, [])
            if isinstance(values, list):
                documentation_items.extend(values)

        documentation_items = list(dict.fromkeys(documentation_items))


# --------------------------
# UI items
# --------------------------

        ui_items = []

        IGNORE_UI = {
            "Search",
            "Take a Tour",
            "+ New Application",
            "Previous",
            "Next",
        }

        for key, value in cleaned.items():

            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, str):
                        continue

                    item = item.strip()

                    if not item:
                        continue

                    if item in IGNORE_UI:
                        continue

                    ui_items.append(item)

            elif isinstance(value, str):

                value = value.strip()

                if value:
                    ui_items.append(value)

        ui_items = list(dict.fromkeys(ui_items))


        print("\nDOCUMENTATION ITEMS")
        for i in documentation_items:
            print("-", i)

        print("\nUI ITEMS")
        for i in ui_items:
            print("-", i)

        matched, missing, extra = self.matcher_ai.match(
            documentation_items,
            ui_items
        )
        # ----------------------------------
        # Component-wise comparison
        # ----------------------------------

        component_results = {}

        components = [
        "headings",
        "table_headers"
        ]
        for component in components:
            expected = documentation.get(component, [])
            actual = cleaned.get(component, [])

            matched_c, missing_c, extra_c = self.component_matcher.compare(
                expected,
                actual
            )

            component_results[component] = {
                "matched": matched_c,
                "missing": missing_c,
                "extra": extra_c
            }

        print("\nFUZZY MATCH RESULT")
        print("Matched :", len(matched))
        print("\nMatched")
        for item in matched:
            print(item.encode("ascii", errors="ignore").decode())

        print()
        print("Missing :", len(missing))
        print("\nMissing")
        for item in missing:
            print(item.encode("ascii", errors="ignore").decode())

        print()
        print("Extra :", len(extra))
        print("\nExtra")
        for item in extra:
            print(item.encode("ascii", errors="ignore").decode())




        print("\n========== COMPONENT SUMMARY ==========")

        for component, result in component_results.items():
            print(f"\n{component.upper()}")
            print("Matched :", len(result["matched"]))
            print("Missing :", len(result["missing"]))
            print("Extra   :", len(result["extra"]))

        # --------------------------
        # Build Prompt
        # --------------------------

        documentation_text = self.section.extract(
            documentation["content"],
            ui["title"]
        )

        print("\n" + "=" * 70)
        print("PAGE:", ui["title"])
        print("=" * 70)

        print("\nDOCUMENTATION SENT TO AI\n")

        print(documentation_text)

        print("=" * 70)

        prompt = self.prompt.build(
            documentation_text,
            cleaned
        )

        # --------------------------
        # Ask AI
        # --------------------------

        try:
            response = self.ai.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

            print("\n========== RAW AI RESPONSE ==========")
            print(result)
            print("\n=====================================\n")

            validated = self.validator.validate(result)

        except Exception as e:
            print("\nAI ERROR")
            print(e)

            validated = {
                "compliance_score": 0,
                "matched": [],
                "missing": [],
                "extra": [],
                "issues": [],
                "summary": "AI comparison skipped because the API request failed."
            }

        # -------------------------------------------------------
        # Fallback if AI returns invalid JSON
        # -------------------------------------------------------

        if validated["compliance_score"] == 0:
            total = len(matched) + len(missing)
            score = 0

            if total > 0:
                score = round((len(matched) / total) * 100)

            validated = {
                "compliance_score": score,
                "matched": matched,
                "missing": missing,
                "extra": extra,
                "issues": [],
                "summary": (
                    "Compliance generated using deterministic fuzzy "
                    "matching because the AI response was invalid."
                )
            }

        # -------------------------------------------------------
        # Automatically generate issues if AI didn't provide them
        # -------------------------------------------------------

        if not validated.get("issues"):
            issues = []
            for item in validated.get("missing", []):
                issues.append({
                    "component": item,
                    "expected": item,
                    "actual": "Not Found",
                    "severity": "Medium",
                    "confidence": 0.90,
                    "guideline_reference": "Documentation",
                    "reason": "Required by documentation but not detected in the UI."
                })
            validated["issues"] = issues

        validated["component_results"] = component_results

        # --------------------------------------------------
        # Keep AI score if valid.
        # Otherwise calculate fuzzy score.
        # --------------------------------------------------

        validated["compliance_score"] = self.score_calculator.calculate(
        matched=validated.get("matched", []),
        missing=validated.get("missing", []),
        extra=validated.get("extra", [])
        )

        return validated