class PromptBuilder:

    def build(self, documentation, ui):

        return f"""
You are a Senior Software QA Engineer performing documentation compliance verification.

Your task is to compare the extracted Website UI against the official documentation.

--------------------------------------------------
OFFICIAL DOCUMENTATION
--------------------------------------------------

{documentation}

--------------------------------------------------
LIVE WEBSITE UI
--------------------------------------------------

{ui}

--------------------------------------------------
IMPORTANT COMPARISON RULES
--------------------------------------------------

1. Compare ONLY features mentioned in the documentation.

2. Ignore completely:
- Sidebar navigation
- User profile
- Notification icons
- Search boxes unless documentation explicitly mentions them
- Dynamic counters (655, 788, etc.)
- Pagination numbers
- Badges
- Tour buttons
- Profile initials
- Logged-in username

3. Treat these as MATCHES:
Facility == Facilities
Application == Applications
FAQ == FAQs
User == Users
Role == User Role
Status Chip == Status Filter
Waiver Type == Application Type

4. Ignore:
- Uppercase/lowercase
- Singular/plural
- Extra spaces
- Minor wording differences

5. If two elements clearly mean the same thing,
count them as MATCHED.

6. Do NOT invent missing elements.

7. Only report something missing if the documentation
explicitly describes it.

8. Compliance Score Guidelines:

100 = Perfect match

90-99 = Almost identical

75-89 = Minor differences

50-74 = Several documented features missing

Below 50 = Major mismatch

--------------------------------------------------
Return ONLY valid JSON.
--------------------------------------------------

{{
    "compliance_score": 0,
    "matched": [
        "..."
    ],
    "missing": [
        "..."
    ],
    "extra": [
        "..."
    ],
    "summary": "Short professional explanation."
}}

IMPORTANT:

Return ONLY JSON.

Do NOT use markdown.

Do NOT use ```json

Do NOT explain your reasoning.

Do NOT add any text before or after the JSON.
"""