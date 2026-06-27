import json

from app.ai.feature_comparator import FeatureComparator

cmp = FeatureComparator()

with open(
    "data/features/my_applications.json",
    encoding="utf-8"
) as f:

    documentation = json.load(f)

with open(
    "data/extracted/my_applications.json",
    encoding="utf-8"
) as f:

    website = json.load(f)

result = cmp.compare(
    documentation,
    website
)

print()

print("Score :", result["compliance_score"])

print()

print("Matched")

for i in result["matched"]:
    print("-", i)

print()

print("Missing")

for i in result["missing"]:
    print("-", i)

print()

print("Extra")

for i in result["extra"]:
    print("-", i)