import re

ARTICLE_RE = re.compile(r"(მუხლი\s+\d+\.)", re.IGNORECASE)
POINT_RE = re.compile(r"(?<!\d)(\d{1,2})\.\s+")

def split_into_articles(pages):
    big = []
    for p in pages:
        big.append(f"\n\n[[PAGE={p['page']}]]\n\n{p['text']}")
    big_text = "".join(big)

    parts = ARTICLE_RE.split(big_text)
    if len(parts) < 3:
        return []

    chunks = []

    for i in range(1, len(parts), 2):
        article_label = parts[i].strip()
        content = parts[i + 1].strip()

        # pages range
        pages_found = [int(x) for x in re.findall(r"\[\[PAGE=(\d+)\]\]", content)]
        page_start = min(pages_found) if pages_found else None
        page_end = max(pages_found) if pages_found else None

        # i remove page markers
        cleaned = re.sub(r"\[\[PAGE=\d+\]\]", "", content).strip()
        if not cleaned:
            continue

        # split article into points
        matches = list(POINT_RE.finditer(cleaned))

        # if no points keep the article as one chunk
        if not matches:
            chunks.append({
                "article": article_label.replace(".", "").strip(),  # "მუხლი 11"
                "section": None,
                "page_start": page_start,
                "page_end": page_end,
                "text": cleaned
            })
            continue


        intro = cleaned[:matches[0].start()].strip()
        if intro:
            chunks.append({
                "article": article_label.replace(".", "").strip(),
                "section": None,
                "page_start": page_start,
                "page_end": page_end,
                "text": intro
            })

        # create chunk for each point
        for idx, m in enumerate(matches):
            point_num = m.group(1)
            start = m.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
            point_text = cleaned[start:end].strip()

            chunks.append({
                "article": article_label.replace(".", "").strip(),
                "section": f"პ.{point_num}",
                "page_start": page_start,
                "page_end": page_end,
                "text": point_text
            })

    return chunks
