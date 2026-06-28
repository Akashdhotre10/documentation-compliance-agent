
import json

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

        documentation_items = []
        documentation_items.append(documentation["title"])
        documentation_items.extend(
            line.strip()
            for line in documentation["content"].split("\n")
            if line.strip()
        )

        # Structured fields (future-proof)
        for key in [
            "buttons",
            "forms",
            "headings",
            "table_headers",
            "cards",
            "badges",
            "tabs"
        ]:
            if key in documentation:
                values = documentation[key]
                if isinstance(values, list):
                    documentation_items.extend(values)
                    documentation_items = list(dict.fromkeys(documentation_items))

        ui_items = []

        for key, value in cleaned.items():
            if isinstance(value, list):
                ui_items.extend(
                    item.strip()
                    for item in value
                    if isinstance(item, str) and item.strip()
                )
            elif isinstance(value, str):
                if value.strip():
                    ui_items.append(value.strip())

        ui_items = list(dict.fromkeys(ui_items))

        # --------------------------
        # RapidFuzz Matching
        # --------------------------

        matched, missing, extra = self.matcher_ai.match(
            documentation_items,
            ui_items
        )

        # ----------------------------------
        # Component-wise comparison
        # ----------------------------------

        component_results = {}

        components = [
            "buttons",
            "forms",
            "headings",
            "table_headers",
            "cards",
            "badges",
            "tabs"
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
        # Calculate deterministic compliance score
        # --------------------------------------------------
        print("\n========== SCORE DEBUG ==========")
        print("Matched :", len(validated.get("matched", [])))
        print("Missing :", len(validated.get("missing", [])))
        print("Extra   :", len(validated.get("extra", [])))
        print("Component Results:", validated.get("component_results"))
        print("=================================\n")

        
        validated["compliance_score"] = self.score_calculator.calculate(
            matched=validated.get("matched", []),
            missing=validated.get("missing", []),
            extra=validated.get("extra", []),
            component_results=validated.get("component_results")
        )

        return validated