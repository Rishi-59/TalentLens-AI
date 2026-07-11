"""
validator.py

Resume PDF validation service.
"""

from pathlib import Path
import re

from pypdf import PdfReader
from pypdf.errors import PdfReadError
from werkzeug.datastructures import FileStorage


class Validator:
    """
    Validates uploaded PDF resumes.
    """

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    SAFE_FILENAME = re.compile(r"^[A-Za-z0-9._ -]+$")

    def __init__(self, file: FileStorage):
        self.file = file

    def _valid_extension(self):
        if Path(self.file.filename).suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are allowed.")

    def _safe_filename(self):
        if not self.SAFE_FILENAME.fullmatch(Path(self.file.filename).name):
            raise ValueError("Filename contains invalid characters.")

    def _non_empty(self):
        self.file.stream.seek(0, 2)
        size = self.file.stream.tell()
        self.file.stream.seek(0)

        if size == 0:
            raise ValueError("Uploaded file is empty.")

    def _file_size(self):
        self.file.stream.seek(0, 2)
        size = self.file.stream.tell()
        self.file.stream.seek(0)

        if size > self.MAX_FILE_SIZE:
            raise ValueError(
                f"Maximum allowed file size is "
                f"{self.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

    def _valid_pdf(self):
        try:
            reader = PdfReader(self.file.stream)

            if len(reader.pages) == 0:
                raise ValueError("PDF contains no pages.")

            if reader.is_encrypted:
                raise ValueError("Password protected PDFs are not supported.")

            self.file.stream.seek(0)

        except PdfReadError:
            raise ValueError("Corrupted or invalid PDF.")

        except Exception as e:
            self.file.stream.seek(0)
            raise ValueError(str(e))

    def validate(self):
        """
        Runs every validation.

        Returns:
            (True, "Valid PDF")
            (False, "Reason")
        """

        try:
            self._valid_extension()
            self._safe_filename()
            self._non_empty()
            self._file_size()
            self._valid_pdf()

            return True, "Valid PDF"

        except Exception as e:
            return False, str(e)