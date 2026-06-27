from app.parser.pdf_parser import PDFParser


pdf = PDFParser("data/guidelines/WaiverPro-User-Guidelines.pdf")

pages = pdf.extract_text()

print("Total Pages:", len(pages))

print()

print(pages[0]["text"][:1000])