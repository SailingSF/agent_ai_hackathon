from composio_openai import ComposioToolSet, Action
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
# Initialize OpenAI client and Composio toolset


openai_client = OpenAI(api_key=os.getenv("OPENAI_LOCAL_API_KEY"))
tool_set = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

tools = tool_set.get_tools(actions=[Action.TWITTER_CREATION_OF_A_POST])

tweet = "This was posted via AI"
task = f"Post this tweet for me: {tweet}"

# Create a chat completion request to OpenAI
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant who posts on X/Twitter when requested."},
        {"role": "user", "content": task},
    ],
)

# Handle the tool calls and print the results
result = tool_set.handle_tool_calls(response)
print("Result:")
print(result)