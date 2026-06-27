import json

from app.matcher.page_matcher import PageMatcher
from app.ai.groq_client import GroqClient
from app.ai.ui_cleaner import UICleaner
from app.ai.prompt_builder import PromptBuilder
from app.ai.json_validator import JSONValidator


class Comparator:

    def __init__(self):

        self.matcher = PageMatcher()

        self.ai = GroqClient()

        self.cleaner = UICleaner()

        self.prompt = PromptBuilder()

        self.validator = JSONValidator()

    def compare_page(self, json_path):

        with open(json_path, encoding="utf-8") as file:
            ui = json.load(file)

        documentation = self.matcher.get_page(
            ui["title"],
        )

        if documentation is None:
            return {
                "compliance_score": 0,
                "matched": [],
                "missing": [],
                "extra": [],
                "summary": f"No documentation found for page '{ui['title']}'"
            }

        cleaned = self.cleaner.clean(ui)

        prompt = self.prompt.build(
            documentation["content"],
            cleaned
        )

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

        return self.validator.validate(result)