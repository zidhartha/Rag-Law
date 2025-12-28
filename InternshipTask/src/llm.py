

from config import LLM_PROVIDED, GROQ_MODEL, OLLAMA_MODEL

def call_llm(prompt: str) -> str:
    if LLM_PROVIDED == "groq":
        from llm_groq import call_groq
        return call_groq(prompt, GROQ_MODEL)

    if LLM_PROVIDED == "ollama":
        from llm_ollama import call_ollama
        return call_ollama(prompt, OLLAMA_MODEL)

    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDED}")