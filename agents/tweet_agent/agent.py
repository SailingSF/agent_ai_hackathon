from composio_openai import ComposioToolSet, Action
from openai import OpenAI
from dotenv import load_dotenv
import os
from classes import Tweet



class TweetAgent:
    def run_agent(tweet: str) -> str:
        task = f"Tweet the following message from my account: {tweet}"

        openai_client = OpenAI(api_key=os.environ.get("OPENAI_LOCAL_API_KEY"))
        tool_set = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        tools = tool_set.get_tools(actions=[Action.TWITTER_CREATION_OF_A_POST])

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

        return result[0].successful
