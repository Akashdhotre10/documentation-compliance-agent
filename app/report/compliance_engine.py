import json
from pathlib import Path

from app.ai.comparator import Comparator
from app.report.report_generator import ReportGenerator


class ComplianceEngine:

    def __init__(self):
        self.comparator = Comparator()
        self.report = ReportGenerator()

    def run(self):
        extracted = Path("data/extracted")
        results = []

        for file in extracted.glob("*.json"):
            with open(file, encoding="utf-8") as f:
                data = json.load(f)

            # Skip non-UI JSON files
            if not isinstance(data, dict):
                continue

            if "title" not in data:
                continue

            print(f"Checking {file.name}...")

            result = self.comparator.compare_page(str(file))

            page_name = file.stem.replace("_", " ").title()

            self.report.generate(result, page_name)

            results.append({
                "page": page_name,
                "score": result["compliance_score"],
                "status": (
                    "PASS" if result["compliance_score"] >= 90
                    else "WARNING" if result["compliance_score"] >= 70
                    else "FAIL"
                ),
            })

        self.generate_dashboard(results)

    def generate_dashboard(self, results):
        html = """
<!DOCTYPE html>

<html>

<head>

<title>Compliance Dashboard</title>

<style>

body{
font-family:Arial;
background:#eef2f7;
padding:40px;
}

table{
width:100%;
border-collapse:collapse;
background:white;
}

th{
background:#2c3e50;
color:white;
padding:15px;
}

td{
padding:15px;
border-bottom:1px solid #ddd;
}

h1{
text-align:center;
}

.score{
font-size:40px;
text-align:center;
margin:20px;
}

</style>

</head>

<body>

<h1>AI Documentation Compliance Dashboard</h1>

<table>

<tr>

<th>Page</th>

<th>Score</th>

<th>Status</th>

</tr>
"""

        total = 0

        for item in results:
            total += item["score"]

            html += f"""

<tr>

<td>{item["page"]}</td>

<td>{item["score"]}%</td>

<td>{item["status"]}</td>

</tr>

"""

        average = round(total / len(results), 2) if results else 0

        html += f"""

</table>

<div class="score">

Overall Compliance

<h2>{average}%</h2>

</div>

</body>

</html>
"""

        with open("reports/index.html", "w", encoding="utf-8") as file:
            file.write(html)

        print("\nDashboard Generated!")