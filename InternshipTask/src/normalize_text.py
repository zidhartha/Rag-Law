import re

URL_LINE_RE = re.compile(r"^https?://\S+.*$", re.MULTILINE)
MATSNE_LINE_RE = re.compile(r"^http://www\.matsne\.gov\.ge.*$", re.MULTILINE)
CODE_LINE_RE = re.compile(r"^\s*040\.\d{3}\.\d{3}\.\d{2}\.\d{3}\.\d{3}\.\d{3}\s*$", re.MULTILINE)

def normalize_text(text: str) -> str:
    text = text.replace("\r", "")

    # remove matsne noise lines
    text = URL_LINE_RE.sub("", text)
    text = MATSNE_LINE_RE.sub("", text)
    text = CODE_LINE_RE.sub("", text)

    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
