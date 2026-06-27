
import json

from app.matcher.page_matcher import PageMatcher
from app.ai.groq_client import GroqClient
from app.ai.ui_cleaner import UICleaner
from app.ai.prompt_builder import PromptBuilder
from app.ai.json_validator import JSONValidator
from app.ai.fuzzy_matcher import FuzzyMatcher
from app.ai.section_extractor import SectionExtractor


class Comparator:

    def __init__(self):

        # Documentation matcher
        self.matcher = PageMatcher()

        self.section = SectionExtractor()

        # RapidFuzz matcher
        self.matcher_ai = FuzzyMatcher()

        # AI
        self.ai = GroqClient()

        self.cleaner = UICleaner()

        self.prompt = PromptBuilder()

        self.validator = JSONValidator()

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

        print("Documentation :", documentation["title"])

        if documentation is None:

            return {
                "compliance_score": 0,
                "matched": [],
                "missing": [],
                "extra": [],
                "summary": f"No documentation found for page '{ui['title']}'"
            }

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
            documentation["content"].split("\n")
        )

        ui_items = []

        for value in cleaned.values():

            if isinstance(value, list):

                ui_items.extend(value)

            elif isinstance(value, str):

                ui_items.append(value)

        # --------------------------
        # RapidFuzz Matching
        # --------------------------

        matched, missing, extra = self.matcher_ai.match(
            documentation_items,
            ui_items
        )

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

        print("\n========== RAW AI RESPONSE ==========\n")
        print(result)
        print("\n=====================================\n")

        validated = self.validator.validate(result)

        # --------------------------
        # Fallback if AI fails
        # --------------------------

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
                "summary": "Compliance generated using deterministic fuzzy matching because the AI response was invalid."
            }

        return validated