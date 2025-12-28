import os
from groq import Groq

def call_groq(prompt: str, model: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it in PyCharm Run Config -> Environment variables."
        )

    client = Groq(api_key=api_key)

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "შენ ხარ სამართლებრივი ასისტენტი. უპასუხე მხოლოდ ქართულად და მხოლოდ მოწოდებული კონტექსტის საფუძველზე."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=2000,
    )
    return resp.choices[0].message.content
