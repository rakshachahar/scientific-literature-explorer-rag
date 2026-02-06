import os
from openai import OpenAI

def generate_answer(prompt: str):

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    try:
        response = client.responses.create(
            model="openai/gpt-4o-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        print("[OPENROUTER ERROR]", e)

        return (
            "⚠️ LLM generation failed.\n\n"
            "Showing retrieved context instead:\n\n"
            f"{prompt}"
        )
