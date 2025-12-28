import numpy as np
import re

# tiny stopword list
STOPWORDS = {
    "რა", "როგორ", "რომ", "თუ", "აქვს", "აქვს?", "არის", "და", "ან", "როდის", "ვის", "პირს"
}

def rerank_results(question, retrieved, top_n=5):
    # basic tokenization
    tokens = re.findall(r"[ა-ჰA-Za-z0-9]+", question.lower())
    keywords = [t for t in tokens if len(t) >= 3 and t not in STOPWORDS]

    if not keywords:

        return sorted(retrieved, key=lambda x: x[1], reverse=True)[:top_n]

    scored = []
    for chunk, orig_score in retrieved:
        text = chunk["text"].lower()
        matches = sum(1 for kw in keywords if kw in text)
        kw_score = matches / len(keywords)
        combined = orig_score * 0.7 + kw_score * 0.3
        scored.append((chunk, combined))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]

# extract domain-specific anchors based on the keywords in the questions
def get_domain_keywords(question):
    q_lower = question.lower()

    # Legal domains with their anchor terms
    domains = {
        'პატივი': 'პირადი არაქონებრივი უფლებები; პატივი; ღირსება; დაცვა;',
        'ღირსება': 'პირადი არაქონებრივი უფლებები; პატივი; ღირსება; დაცვა;',
        'უფლებაუნარიანობა': 'უფლებაუნარიანობა; ფიზიკური პირი; დაბადება; გარდაცვალება;',
        'ქორწინება': 'ქორწინება; ოჯახი; მეუღლე; ქორწინების რეგისტრაცია;',
        'მემკვიდრეობა': 'მემკვიდრეობა; მამკვიდრებელი; მემკვიდრე; სამკვიდრო;',
        'ხელშეკრულება': 'ხელშეკრულება; გარიგება; ვალდებულება; შესრულება;',
        'საკუთრება': 'საკუთრების უფლება; მესაკუთრე; ნივთი; საკუთრება;',
    }

    for keyword, anchors in domains.items():
        if keyword in q_lower:
            return anchors

    return 'საქართველოს სამოქალაქო კოდექსი; სამართლებრივი დაცვა;'

# retrieve and rerank relevant chunks
def retrieve(embedder, index, chunks, question, top_k=20, top_n=5):


    anchors = get_domain_keywords(question)

    # Multiple query formulations
    queries = [
        f"query: {question}",
        f"query: {anchors} {question}",
    ]

    # Encode queries
    q_embeddings = embedder.encode(
        queries,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    # Average embeddings
    q = np.mean(q_embeddings, axis=0, keepdims=True)

    scores, idxs = index.search(q, top_k)

    results = []
    for score, idx in zip(scores[0], idxs[0]):
        if idx == -1:
            continue
        results.append((chunks[idx], float(score)))

    # Rerank and return top_n
    return rerank_results(question, results, top_n=top_n)
