from composio_openai import ComposioToolSet, Action
from together import Together
from dontenv import load_dotenv
load_dotenv()


def main():
    tool_set = ComposioToolSet()
    tools = tool_set.get_tools(actions=[Action.TWITTER_CREATION_OF_A_POST])

    client = Together(api_key=api_key)

    response = client.chat.completions.create(
        model = model,
        tools = tools
        tool_choice = 'auto',
        
    )
    


if __name__ == "__main__":
    main()


