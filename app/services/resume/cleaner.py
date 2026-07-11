"""
cleaner.py

Responsible for cleaning raw text extracted from PDF files.
"""

import re


class TextCleaner:
    """
    Cleans raw extracted PDF text.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Normalize extracted text.

        Operations:
        - Normalize line endings
        - Remove trailing spaces
        - Collapse multiple blank lines
        - Remove repeated spaces
        """

        # Windows -> Unix line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove trailing spaces/tabs
        text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

        # Replace multiple spaces/tabs with one space
        text = re.sub(r"[ \t]{2,}", " ", text)

        # Collapse 3+ blank lines into 2
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text