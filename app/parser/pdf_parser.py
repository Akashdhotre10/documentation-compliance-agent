import fitz  # PyMuPDF
from pathlib import Path


class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        """
        Reads the PDF and extracts text page by page.
        """

        document = fitz.open(self.pdf_path)

        pages = []

        for page_number, page in enumerate(document):

            text = page.get_text("text")

            pages.append({
                "page": page_number + 1,
                "text": text
            })

        document.close()

        return pages