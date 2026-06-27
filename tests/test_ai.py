from app.ai.comparator import Comparator
from app.report.report_generator import ReportGenerator

comparator = Comparator()

result = comparator.compare_page(
    "data/extracted/my_applications.json"
)

print(result)

report = ReportGenerator()

filename = report.generate(
    result,
    "My Applications"
)

print(f"\nReport saved to: {filename}")