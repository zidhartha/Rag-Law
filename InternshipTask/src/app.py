import os
from config import PDF_PATH, INDEX_PATH, CHUNKS_PATH, EMBED_MODEL, TOP_K, MIN_SIMILARITY, OLLAMA_MODEL
from embedding import build_and_save_index, load_index_and_chunks
from retrieve import retrieve
from prompt import format_context, build_prompt
from dotenv import load_dotenv

load_dotenv()
from validate import should_abstain, allowed_citations, validate_answer
from llm import call_llm

ABSTAIN_TEXT = "მოცემული ამონარიდებით ზუსტი პასუხი ვერ დასტურდება საქართველოს სამოქალაქო კოდექსში."

from pathlib import Path
import json

from ingest import extract_pages
from chunking import split_into_articles
from embedding import build_and_save_index


def ensure_index():
    # if both files exist we analyze the schema.
    if INDEX_PATH.exists() and CHUNKS_PATH.exists():
        try:
            with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            # if new schema we dont analyze and build.
            if chunks and "section" in chunks[0]:
                print("Index already exists and schema is valid.")
                return

            print("Old chunks schema detected. Rebuilding index...")

        except Exception:
            print("Failed to read chunks.json. Rebuilding index...")

        INDEX_PATH.unlink(missing_ok=True)
        CHUNKS_PATH.unlink(missing_ok=True)

    # building an index
    print("Index not found. Building index from PDF...")
    pages = extract_pages(PDF_PATH)
    chunks = split_into_articles(pages)

    if not chunks:
        raise RuntimeError("Chunking failed: no chunks produced.")

    build_and_save_index(
        chunks,
        EMBED_MODEL,
        str(INDEX_PATH),
        str(CHUNKS_PATH)
    )

    print(f"Index built successfully. Chunks count: {len(chunks)}")


def main():
    ensure_index()
    embedder, index, chunks = load_index_and_chunks(EMBED_MODEL, INDEX_PATH, CHUNKS_PATH)
    print("Sample chunk keys:", chunks[0].keys())
    print("Sample section:", chunks[0].get("section"))

    while True:
        q = input("\nკითხვა (Enter to exit): ").strip()
        if not q:
            break

        retrieved = retrieve(embedder, index, chunks, q, TOP_K)
        print("\n--- Retrieval debug ---")
        for c, s in retrieved:
            preview = c["text"].replace("\n", " ")[:120]
            print("HIT:", c["article"], "score=", round(s, 3), "preview=", preview)
        print("--- end ---\n")

        if should_abstain(retrieved, MIN_SIMILARITY):
            print("\n" + ABSTAIN_TEXT)
            continue

        context = format_context(retrieved)
        prompt = build_prompt(q, context)

        answer = call_llm(prompt)

        allowed = allowed_citations(retrieved)
        answer = validate_answer(answer, allowed)

        print("\n" + answer)


if __name__ == "__main__":
    main()
