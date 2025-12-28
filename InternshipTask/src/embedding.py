import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def build_and_save_index(chunks,model_name,index_path,chunks_path):
    os.makedirs(os.path.dirname(index_path),exist_ok=True)

    embedder = SentenceTransformer(model_name)
    texts = [c['text'] for c in chunks]
    passages = [f"passage: {t}" for t in texts]

    embedding = embedder.encode(
        passages,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    ).astype('float32')

    dimension = embedding.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding)

    faiss.write_index(index,str(index_path))

    with open(str(chunks_path),'w',encoding='utf-8') as f:
        json.dump(chunks,f,ensure_ascii=False,indent=2)


def load_index_and_chunks(model_name,index_path,chunks_path):
    embedder = SentenceTransformer(model_name)
    index = faiss.read_index(str(index_path))

    with open(str(chunks_path),'r',encoding ='utf-8') as f:
        chunks = json.load(f)

    return embedder,index,chunks