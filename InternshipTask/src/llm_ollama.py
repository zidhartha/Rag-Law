import requests


def call_ollama(prompt, model):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=180
    )
    r.raise_for_status()
    return r.json()['response']
