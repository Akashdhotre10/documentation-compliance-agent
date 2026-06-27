import re


class UICleaner:

    def clean(self, ui):

        cleaned = {}

        for key, values in ui.items():

            if not isinstance(values, list):
                cleaned[key] = values
                continue

            new_values = []

            for item in values:

                if not item:
                    continue

                item = str(item)

                # Remove numbers
                item = re.sub(r"\d+", "", item)

                # Remove extra spaces
                item = re.sub(r"\s+", " ", item)

                item = item.strip()

                if len(item) < 2:
                    continue

                new_values.append(item)

            cleaned[key] = sorted(set(new_values))

        return cleaned