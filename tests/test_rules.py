from app.parser.pdf_parser import PDFParser
from app.parser.rule_extractor import RuleExtractor


pdf = PDFParser("data/guidelines/WaiverPro-User-Guidelines.pdf")

pages = pdf.extract_text()

extractor = RuleExtractor(pages)

sections = extractor.extract_sections()

print("Total Sections:", len(sections))

print()

print(sections[0])