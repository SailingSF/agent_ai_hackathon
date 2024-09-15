from composio_openai import ComposioToolSet, Action
from openai import OpenAI

# Initialize OpenAI client and Composio toolset
openai_client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
composio_toolset = ComposioToolSet(api_key="YOUR_COMPOSIO_API_KEY")

# Define the task to retrieve tweets from a space
space_id = "YOUR_TWITTER_SPACE_ID"  # Replace with your actual Twitter space ID
task = f"Retrieve tweets from space {space_id}"

# Get the necessary tools for Twitter actions
tools = composio_toolset.get_tools(actions=[Action.TWITTER_RETRIEVE_POSTS_FROM_A_SPACE])

# Create a chat completion request to OpenAI
response = openai_client.chat.completions.create(
    model="gpt-4-turbo-preview",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)

# Handle the tool calls and print the results
result = composio_toolset.handle_tool_calls(response)
print("Retrieved Tweets:")
print(result)