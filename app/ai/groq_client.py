import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def compare(self, documentation, ui_json):

        prompt = f"""
You are an expert Documentation Compliance AI.

Compare the DOCUMENTATION with the WEBSITE UI.

DOCUMENTATION:

{documentation}

---------------------------------------

WEBSITE UI:

{ui_json}

---------------------------------------

Return ONLY valid JSON in this format:

{{
    "compliance_score": 0,
    "matched": [],
    "missing": [],
    "extra": [],
    "summary": ""
}}

Do not return markdown.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content