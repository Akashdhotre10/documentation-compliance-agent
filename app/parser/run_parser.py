from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.parser.pdf_parser import PDFParser
from app.parser.rule_extractor import RuleExtractor
from app.parser.documentation_analyzer import DocumentationAnalyzer
from app.parser.json_writer import JSONWriter


pdf = PDFParser("data/guidelines/WaiverPro-User-Guidelines.pdf")

pages = pdf.extract_text()

extractor = RuleExtractor(pages)

sections = extractor.extract_sections()

# --------------------------------------
# Analyze documentation
# --------------------------------------

analyzer = DocumentationAnalyzer()

structured_sections = []

for section in sections:
    structured_sections.append(
        analyzer.analyze(section)
    )

JSONWriter.save(
    structured_sections,
    "data/extracted/guidelines.json"
)