import re


class DocumentationAnalyzer:
    """
    Converts documentation text into structured UI components.
    """
    def analyze(self, section):
        structured = section.copy()

        content = section.get("content", "")

        structured["buttons"] = self.extract_buttons(content)
        structured["table_headers"] = self.extract_table_headers(content)
        structured["forms"] = self.extract_forms(content)
        structured["charts"] = self.extract_charts(content)
        structured["cards"] = self.extract_cards(content)
        structured["tabs"] = self.extract_tabs(content)
        structured["badges"] = self.extract_badges(content)

        return structured

    # ------------------------------------------------

    def extract_buttons(self, text):
        buttons = []

        patterns = [
            r"Click\s+([A-Za-z0-9+ ]+)",
            r"button\s+([A-Za-z0-9+ ]+)",
            r"Use\s+([A-Za-z0-9+ ]+)",
            r"select\s+([A-Za-z0-9+ ]+)"
        ]

        for pattern in patterns:
            for match in re.findall(pattern, text, re.IGNORECASE):
                value = match.strip()
                if len(value) < 40:
                    buttons.append(value)

        return sorted(set(buttons))
    # ------------------------------------------------

    def extract_table_headers(self, text):
        headers = []

        patterns = [
            r"columns?\s+(.*?)(?:\.|\n)",
            r"listed with the columns\s+(.*?)(?:\.|\n)",
            r"table lists.*?columns\s+(.*?)(?:\.|\n)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                continue

            items = re.split(r",|and", match.group(1))
            for item in items:
                item = item.strip()
                item = item.replace("the columns", "")
                item = item.replace("columns", "")
                if len(item) > 1:
                    headers.append(item)

        return sorted(set(headers))
    # ------------------------------------------------

    def extract_forms(self, text):
        forms = []

        keywords = [
            "Status",
            "Priority",
            "Name",
            "Email",
            "Password",
            "Facility",
            "Role",
            "Search"
        ]

        for word in keywords:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                forms.append(word)

        return sorted(set(forms))

    # ------------------------------------------------

    def extract_charts(self, text):
        charts = []

        chart_types = [
            "chart",
            "graph",
            "doughnut",
            "pie",
            "bar",
            "line"
        ]

        for chart in chart_types:
            if re.search(rf"\b{chart}\b", text, re.IGNORECASE):
                charts.append(chart)

        return sorted(set(charts))

    def extract_tabs(self, text):
        tabs = []

        match = re.search(
            r"tabs?\s+[—:-]?\s*(.*?)(?:\.|\n)",
            text,
            re.IGNORECASE
        )

        if match:
            items = re.split(r",|and", match.group(1))
            tabs.extend(i.strip() for i in items if i.strip())

        return sorted(set(tabs))

    def extract_cards(self, text):
        cards = []

        keywords = [
            "card",
            "cards",
            "Profile Information",
            "Organisation",
            "Notifications",
            "Security",
            "Features",
            "Applications Overview",
            "Facilities Status Overview"
        ]

        for word in keywords:
            if word.lower() in text.lower():
                cards.append(word)

        return sorted(set(cards))

    def extract_badges(self, text):
        badges = []

        values = [
            "Active",
            "Upcoming",
            "Expired",
            "Draft",
            "Submitted",
            "Approved",
            "Rejected",
            "Done",
            "In Process",
            "High",
            "Medium",
            "Low"
        ]

        for value in values:
            if re.search(rf"\b{re.escape(value)}\b", text, re.IGNORECASE):
                badges.append(value)

        return sorted(set(badges))