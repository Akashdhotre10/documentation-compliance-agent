from app.report.coverage_calculator import CoverageCalculator
from pathlib import Path
from datetime import datetime


class ReportGenerator:

    def progress_bar(self, score):

        filled = int(score / 5)

        return "█" * filled + "░" * (20 - filled)

    def generate(self, result, page_name, component_results=None):
        reports = Path("reports")
        reports.mkdir(exist_ok=True)

        score = result["compliance_score"]

        # ---------------------------------------
        # Screenshot Path & report filename normalization
        # - Ensure pages like 'action_items' and 'action_items_report'
        #   produce a single report file (we normalize to a base name).
        # - Prefer an existing screenshot file; if none exists, show placeholder text.
        # ---------------------------------------

        base_name = page_name.lower().replace(" ", "_")
        if base_name.endswith("_report"):
            base_name = base_name[: -len("_report")]

        # Prefer screenshot named after base_name, but also accept base_name + '_report'
        image_candidates = [f"{base_name}.png", f"{base_name}_report.png"]
        image_path = None
        for candidate in image_candidates:
            candidate_path = Path("screenshots") / candidate
            if candidate_path.exists():
                # Use relative path from reports/ folder
                image_path = f"../screenshots/{candidate}"
                break

        # Build screenshot HTML (show placeholder if missing)
        if image_path:
            screenshot_html = f"""
            <div class="card">
            <h2>Captured Screenshot</h2>

            <img src="{image_path}" style="width:100%;border-radius:10px;border:1px solid #ddd;" />

            </div>
            """
        else:
            screenshot_html = """
            <div class="card">
            <h2>Captured Screenshot</h2>
            <p><em>No screenshot available for this page.</em></p>
            </div>
            """


        coverage_html = ""

        if component_results:
            calculator = CoverageCalculator()
            coverage, overall = calculator.calculate(component_results)
            coverage_html = """
            <div class="card">
            <h2>Coverage Report</h2>

            <table style="width:100%;border-collapse:collapse;">
                <tr>
                    <th align="left">Component</th>
                    <th align="center">Matched</th>
                    <th align="center">Expected</th>
                    <th align="center">Coverage</th>
                </tr>
            """

            for component, data in coverage.items():
                coverage_html += f"""
                <tr>
                    <td>{component.title()}</td>
                    <td align="center">{data['matched']}</td>
                    <td align="center">{data['expected']}</td>
                    <td align="center">{data['coverage']}%</td>
                </tr>
                """

            coverage_html += "</table></div>"

        # ---------------------------------------
        # Statistics
        # ---------------------------------------

        matched_count = len(result.get("matched", []))
        missing_count = len(result.get("missing", []))
        extra_count = len(result.get("extra", []))

        issues = result.get("issues", [])

        # ---------------------------------------
        # Build Discrepancy Table
        # ---------------------------------------

        issues_html = ""

        if issues:
            issues_html = """
            <div class="card">
            <h2>Discrepancy Report</h2>

            <table style="width:100%;border-collapse:collapse;">

            <tr style="background:#f2f2f2;">
                <th>Component</th>
                <th>Expected</th>
                <th>Actual</th>
                <th>Severity</th>
                <th>Confidence</th>
            </tr>
            """

            for issue in issues:
                severity = issue.get("severity", "Medium")
                color = {
                    "Low": "#2ecc71",
                    "Medium": "#f39c12",
                    "High": "#e74c3c"
                }.get(severity, "#3498db")

                issues_html += f"""
                <tr>
                    <td>{issue.get('component','')}</td>
                    <td>{issue.get('expected','')}</td>
                    <td>{issue.get('actual','')}</td>
                    <td style="color:{color};font-weight:bold;">{severity}</td>
                    <td>{round(issue.get('confidence',0)*100)}%</td>
                </tr>
                """

            issues_html += "</table></div>"

        # Backward compatibility
        if not issues:
            for item in result.get("missing", []):
                issues.append({
                    "component": item,
                    "expected": item,
                    "actual": "Not Found",
                    "severity": "Medium",
                    "confidence": 0.90,
                    "guideline_reference": "Documentation",
                    "reason": result.get("summary", "")
                })

        if score >= 90:
            color = "#2ecc71"
            status = "PASS"
        elif score >= 70:
            color = "#f39c12"
            status = "WARNING"
        else:
            color = "#e74c3c"
            status = "FAIL"

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Compliance Report</title>
<style>
body {{
    background: #eef2f7;
    font-family: Arial;
    padding: 40px;
}}

.container {{
    background: white;
    max-width: 1100px;
    margin: auto;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,.15);
}}

.header {{
    text-align: center;
    margin-bottom: 30px;
}}

.score {{
    font-size: 60px;
    font-weight: bold;
    color: {color};
}}

.bar {{
    font-size: 28px;
    margin-bottom: 20px;
}}

.card {{
    background: #fafafa;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
    border-left: 6px solid {color};
}}

li {{
    padding: 8px;
}}

.footer {{
    margin-top: 40px;
    text-align: center;
    color: gray;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th {{
    background: #3498db;
    color: white;
    padding: 12px;
    text-align: left;
}}

td {{
    padding: 10px;
    border: 1px solid #ddd;
}}

tr:nth-child(even) {{
    background: #f8f8f8;
}}

.stats {{
    display: flex;
    justify-content: space-around;
    margin-top: 25px;
    margin-bottom: 25px;
}}

.stat-card {{
    background: #f7f7f7;
    padding: 15px;
    border-radius: 10px;
    width: 22%;
    text-align: center;
    box-shadow: 0 0 6px rgba(0,0,0,.08);
}}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>AI Documentation Compliance Report</h1>
<p><b>Generated:</b> {datetime.now().strftime("%d %B %Y %H:%M")}</p>
</div>
<div class="score">
{score}%
</div>
<div class="bar">
{self.progress_bar(score)}
</div>
<h2>Status: {status}</h2>
<hr>
<div class="stats">
<div class="stat-card">
<h3>Matched</h3>
<h2>{matched_count}</h2>
</div>
<div class="stat-card">
<h3>Missing</h3>
<h2>{missing_count}</h2>
</div>
<div class="stat-card">
<h3>Extra</h3>
<h2>{extra_count}</h2>
</div>
<div class="stat-card">
<h3>Compliance</h3>
<h2>{score}%</h2>
</div>
</div>
<h2>Page</h2>

<p>{page_name}</p>

{screenshot_html}
<div class="card">
<h2>Matched Elements</h2>
<ul>
{"".join(f"<li>✅ {i}</li>" for i in result["matched"])}
</ul>
</div>
<div class="card">
<h2>Missing Elements</h2>
<ul>
{"".join(f"<li>❌ {i}</li>" for i in result["missing"])}
</ul>
</div>
<div class="card">
<h2>Extra Elements</h2>
<ul>
{"".join(f"<li>⚠ {i}</li>" for i in result["extra"])}
</ul>
</div>
<div class="card">
<h2>Detailed Discrepancy Report</h2>
<table>
<tr>
<th>Component</th>
<th>Expected</th>
<th>Actual</th>
<th>Severity</th>
<th>Confidence</th>
</tr>
{"".join(f"<tr><td>{issue['component']}</td><td>{issue['expected']}</td><td>{issue['actual']}</td><td>{issue['severity']}</td><td>{round(issue['confidence']*100)}%</td></tr>" for issue in issues)}
</table>
</div>
<div class="card">
<h2>AI Recommendation</h2>
<p>
{result.get("summary", "No summary available")}
</p>
</div>
{coverage_html}
{issues_html}
<div class="card">
<h2>Evidence</h2>
<p>
Screenshot support will be added in the next milestone.
</p>
</div>
<div class="footer">
Generated by
<h3>AI Documentation Compliance Agent</h3>
</div>
</div>
</body>
</html>
"""
      

        # Write report using normalized base name; append '_report' to clarify this is a report
        filename = reports / f"{base_name}_report.html"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        return filename