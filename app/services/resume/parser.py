"""
parser.py

Extract raw text from PDF documents.
"""

import fitz  # PyMuPDF
from werkzeug.datastructures import FileStorage


class Parser:
    """Extracts raw text from PDF files."""

    def __init__(self, file: FileStorage):
        self.file = file

    def _open_document(self):
        pdf_bytes = self.file.read()
        self.file.stream.seek(0)

        return fitz.open(stream=pdf_bytes, filetype="pdf")

    def extract_text(self) -> tuple[str, int]:
        """
        Extract raw text exactly as it exists in the PDF.
        No cleaning or formatting is performed.

        Returns:
            (text, page_count)
        """

        document = self._open_document()

        try:
            text = ""

            for page in document:
                text += page.get_text()

            return text, len(document)

        finally:
            document.close()