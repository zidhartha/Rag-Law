import re
import fitz
from normalize_text import normalize_text

# used for getting raw text from the pdf file.
def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        text = doc[i].get_text('text')
        text = normalize_text(text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        pages.append({"page": i + 1, "text": text})
    return pages
