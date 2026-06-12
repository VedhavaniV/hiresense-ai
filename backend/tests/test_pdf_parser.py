import unittest

from app.pdf_parser import PdfExtractionError, extract_text_from_pdf


class PdfParserTests(unittest.TestCase):
    def test_rejects_invalid_pdf_bytes(self):
        with self.assertRaises(PdfExtractionError):
            extract_text_from_pdf(b"this is not a pdf")


if __name__ == "__main__":
    unittest.main()
