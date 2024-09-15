import os, json
from dotenv import load_dotenv
from together import Together
import logging
logger = logging.getLogger(__name__)
load_dotenv()

class Agent:
    def __init__(self, name: str, system_prompt: str, model: str, tools: list[dict] = [], tools_map: dict = {}):
        api_key = os.environ.get("TOGETHER_API_KEY")
        self.name = name
        self.client = Together(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools
        self.tools_map = tools_map
        self.messages = []

    def submit_message(self, prompt: str) -> str:

        new_message = {"role": "user", "content": prompt}
        self.messages.append(new_message)

        completion = self._get_completion()

        tool_calls = completion.choices[0].message.tool_calls
        while tool_calls:
            logger.debug(f"Tool calls present.\n\n{tool_calls}")
            self.messages.append(completion.choices[0].message)  # extend conversation with assistant's reply
            # handle tool call
            completion = self._handle_tool_call(tool_calls)
            tool_calls = completion.choices[0].message.tool_calls
        logger.debug(f"No more tool calls for run of {self.name} agent")

        return completion.choices[0].message.content

    def _handle_tool_call(self, tool_calls):
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.tools_map[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response_json: str
            logger.debug(f"Trying to run function: {function_name} with arguments of {function_args}")
            try:
                function_response = function_to_call(**function_args)
                function_response_json = json.dumps(function_response)
            except Exception as e:
                function_response_json = json.dumps(
                    {
                        "error": str(e),
                    }
                )

            self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response_json,
                }
            )  # extend conversation with function response

        return self._get_completion()

    def _get_completion(self, tool_choice: str = "auto", max_tokens: int = 512, temp: float = 0.5, repitition_pen: float = 1.0):

        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools = self.tools,
            max_tokens=max_tokens,
            temperature=temp,
            repitition_penalty=repitition_pen,
            tool_choice=tool_choice
        )

    def __str__(self) -> str:
        tools_info = ", ".join([tool["function"]["name"] for tool in self.tools]) if self.tools else "None"
        messages_info = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.messages])
        
        return f"Agent Information:\n" \
               f"Name: {self.name}\n" \
               f"Model: {self.model}\n" \
               f"Tools: {tools_info}\n" \
               f"Current Messages:\n{messages_info}"

