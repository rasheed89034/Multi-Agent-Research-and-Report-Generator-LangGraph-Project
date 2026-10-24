from io import BytesIO
from pypdf import PdfReader


def pdf_to_text(data: bytes, max_pages: int = 30) -> str:
    try:
        reader = PdfReader(BytesIO(data))
        return " ".join((p.extract_text() or "") for p in reader.pages[:max_pages])
    except Exception:
        return ""
