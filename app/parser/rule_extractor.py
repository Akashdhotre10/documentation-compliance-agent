import re


class RuleExtractor:

    def __init__(self, pages):
        self.pages = pages

    def extract_sections(self):
        sections = []
        current = None

        for page in self.pages:
            lines = page["text"].splitlines()

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue

                normalized = re.sub(r"\s+", " ", line)

                if self._is_section_header(normalized):
                    if current and self._is_meaningful_section(current):
                        sections.append(current)
                    current = {
    "title": "",
    "content": "",
    "page": page["page"],

    "buttons": [],
    "forms": [],
    "table_headers": [],
    "cards": [],
    "tabs": [],
    "badges": [],
    "charts": []
}
                    continue

                if current is None:
                    continue

                if current["title"] == "" and self._looks_like_title(normalized):
                    current["title"] = normalized
                    continue

                if self._is_noise_line(normalized):
                    continue

                current["content"] += normalized + "\n"

        if current and self._is_meaningful_section(current):
            sections.append(current)

        return sections

    def _is_section_header(self, line):
        return bool(re.search(r"^(S\s+E\s+C\s+T\s+I\s+O\s+N|SECTION)\s*\d+", line, re.IGNORECASE))

    def _looks_like_title(self, line):
        if not line or len(line) > 80:
            return False
        if line.lower().startswith(("url", "figure", "table", "section")):
            return False
        if re.match(r"^\d+\.\s", line):
            return False
        if re.search(r"[A-Za-z]", line) and len(line.split()) <= 8:
            return True
        return False

    def _is_noise_line(self, line):
        lower = line.lower()
        return lower.startswith(("figure", "table", "section")) or lower.startswith("page") or lower.startswith("document")

    def _is_meaningful_section(self, section):
        title = section["title"].strip()
        content = section["content"].strip()
        if not title or not content:
            return False
        if len(content.split()) < 8:
            return False
        return True