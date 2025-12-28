from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PDF_PATH = BASE_DIR / "data" / "matsne-31702-134.pdf"
INDEX_PATH = BASE_DIR / "storage" / "faiss.index"
CHUNKS_PATH = BASE_DIR / "storage" / "chunks.json"


TOP_K = 10
MIN_SIMILARITY = 0.2
EMBED_MODEL = "intfloat/multilingual-e5-large"
LLM_PROVIDED = 'groq'
GROQ_MODEL = "llama-3.3-70b-versatile"
OLLAMA_MODEL = 'qwen2.5:3b'
