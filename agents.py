import os
from dotenv import load_dotenv
from together import Together

load_dotenv()

class Agent:
    def __init__(self, system_prompt: str, model: str, tools: list[dict] = []):
        api_key = os.environ.get("TOGETHER_API_KEY")
        self.client = Together(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools
        self.messages = []

    def submit_message(self, prompt: str) -> str:

        new_message = {"role": "user", "content": prompt}
        self.messages.append(new_message)

        run = self._run_response()

        return run.choices[0].message.content

    def _run_response(self):

        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=512,
            temperature=0.5,
            repitition_penalty=1,
        )

