import os
from together import Together


MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
MAX_TOKENS = 512


def get_client():
    api_key = os.environ.get("TOGETHER_API_KEY")
    print("api key is", api_key)
    return Together(api_key=api_key)


def query_together(prompt: str):
    client = get_client()
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.5,
    )
