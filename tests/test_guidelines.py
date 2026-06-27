import json

with open(
    "data/extracted/guidelines.json",
    encoding="utf-8"
) as f:

    pages = json.load(f)

print("\nTOTAL PAGES:", len(pages))
print()

for page in pages:

    print(page["title"])