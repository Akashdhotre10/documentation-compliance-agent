import json


class PromptBuilder:

    def build(self, documentation, ui):

        prompt = f"""
You are a Senior QA Automation Engineer.

Your task is to compare a web page against its official documentation.

IMPORTANT RULES

1. Ignore:
   - Sidebar navigation
   - Header
   - Footer
   - Notifications
   - User avatar
   - Global navigation

2. Compare ONLY:
   - Page title
   - Headings
   - Buttons
   - Search boxes
   - Tables
   - Table headers
   - Filters
   - Charts
   - Forms

3. Do NOT guess.

4. If an element is present but named slightly differently,
   consider it MATCHED.

5. Compliance score must be an integer between 0 and 100.

DOCUMENTATION

{documentation}

---------------------------------------

WEBSITE UI

{json.dumps(ui, indent=4)}

---------------------------------------

Return ONLY valid JSON.

Do NOT explain your reasoning.

Do NOT write paragraphs.

Do NOT use markdown.

Do NOT use ```json blocks.

Output must start with {{

Output must end with }}

Return exactly this format:

{{
    "compliance_score": 0,
    "matched": [],
    "missing": [],
    "extra": [],
    "summary": ""
}}
"""

        return prompt