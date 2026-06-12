from __future__ import annotations

import logging
from io import BytesIO

from pypdf import PdfReader


class PdfExtractionError(ValueError):
    """Raised when a resume PDF cannot produce usable text."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    logging.getLogger("pypdf").setLevel(logging.ERROR)

    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:
        raise PdfExtractionError("The uploaded file could not be read as a PDF.") from exc

    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n".join(pages).strip()
    if not text:
        raise PdfExtractionError("No readable text was found in the uploaded PDF.")

    return text
