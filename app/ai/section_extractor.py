import re


class SectionExtractor:

    def extract(self, documentation, page_title):

        title = page_title.lower()

        # Direct match
        if title in documentation.lower():
            return self.extract_section(documentation, page_title)

        # Support pages
        if title in ["tickets", "contact", "faqs", "faq"]:
            return self.extract_section(
                documentation,
                "Support"
            )

        return documentation

    def extract_section(self, documentation, heading):

        lines = documentation.split("\n")

        start = None

        for i, line in enumerate(lines):

            if heading.lower() in line.lower():

                start = i

                break

        if start is None:
            return documentation

        result = []

        result.append(lines[start])

        for line in lines[start + 1:]:

            # Stop when another page heading begins
            if re.match(
                r"^[A-Z][A-Za-z0-9\s&—\-]{3,}$",
                line.strip()
            ):
                break

            result.append(line)

        return "\n".join(result)