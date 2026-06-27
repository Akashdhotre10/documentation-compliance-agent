from app.ai.comparator import Comparator

comparator = Comparator()

result = comparator.compare_page(
    "data/extracted/user_management.json"
)

print(result)