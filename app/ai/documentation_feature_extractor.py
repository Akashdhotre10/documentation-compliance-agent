import re


class DocumentationFeatureExtractor:
    """
    Extract structured UI features from documentation text.
    """

    def extract(self, documentation):

        features = {
            "headings": [],
            "buttons": [],
            "forms": [],
            "table_headers": [],
            "cards": [],
            "charts": [],
            "search_boxes": [],
            "tabs": []
        }

        if not documentation:
            return features

        lines = documentation.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Remove bullets
            line = line.replace("•", "")
            line = line.replace("-", "")

            # ---------------------------------
            # Buttons
            # ---------------------------------

            if "button" in line.lower():

                features["buttons"].append(
                    self.clean(line)
                )

            # ---------------------------------
            # Search
            # ---------------------------------

            if "search" in line.lower():

                features["search_boxes"].append("Search")

            # ---------------------------------
            # Forms
            # ---------------------------------

            if (
                "form" in line.lower()
                or "field" in line.lower()
                or "input" in line.lower()
            ):
                features["forms"].append(
                    self.clean(line)
                )

            # ---------------------------------
            # Tables
            # ---------------------------------

            if (
                "column" in line.lower()
                or "table" in line.lower()
            ):

                columns = re.findall(
                    r"[A-Za-z ]+",
                    line
                )

                for col in columns:

                    col = col.strip()

                    if len(col) > 2:
                        features["table_headers"].append(col)

            # ---------------------------------
            # Charts
            # ---------------------------------

            if (
                "chart" in line.lower()
                or "graph" in line.lower()
                or "doughnut" in line.lower()
            ):

                features["charts"].append(
                    self.clean(line)
                )

            # ---------------------------------
            # Cards
            # ---------------------------------

            if "card" in line.lower():

                features["cards"].append(
                    self.clean(line)
                )

        # Remove duplicates

        for key in features:

            features[key] = sorted(
                list(
                    set(features[key])
                )
            )

        return features

    def clean(self, text):

        text = re.sub(r"\s+", " ", text)

        return text.strip()