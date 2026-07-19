#!/usr/bin/env python3

import os
from groq import Groq

class GroqEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found.")

        self.client = Groq(api_key=api_key)

    def ask(self, prompt, model="openai/gpt-oss-120b"):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    engine = GroqEngine()
    answer = engine.ask("Say hello in one sentence.")
    print("\nGroq replied:\n")
    print(answer)
