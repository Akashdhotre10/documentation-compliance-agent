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
        structured["cards"] = []
        structured["tabs"] = []
        structured["badges"] = []

        return structured

    # ------------------------------------------------

    def extract_buttons(self, text):

        buttons = []

        keywords = [
            "Add",
            "Create",
            "Save",
            "Submit",
            "Cancel",
            "Filter",
            "Search",
            "Export",
            "Import",
            "Edit",
            "Delete"
        ]

        for word in keywords:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                buttons.append(word)

        return sorted(set(buttons))

    # ------------------------------------------------

    def extract_table_headers(self, text):

        headers = []

        match = re.search(
            r"columns?\s+(.*?)(?:\.|\n)",
            text,
            re.IGNORECASE
        )

        if match:

            items = re.split(
                r",|and",
                match.group(1)
            )

            for item in items:

                item = item.strip()

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