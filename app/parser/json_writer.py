import json
from pathlib import Path


class JSONWriter:

    @staticmethod
    def save(data, output_path):

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"Saved to {output_path}")