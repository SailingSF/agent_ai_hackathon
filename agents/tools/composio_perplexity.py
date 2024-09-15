from composio_langchain import ComposioToolSet, Action
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# Initialize Composio tool set
tool_set = ComposioToolSet()

# Get Composio's Perplexity AI Search tool and other tools
tools = tool_set.get_tools(actions=[
    Action.PERPLEXITYAI_PERPLEXITY_AI_SEARCH,
    Action.GOOGLE_SEARCH,
    Action.GITHUB_SEARCH,
    # Add more tools as needed
])

# Initialize the language model
llm = OpenAI(temperature=0)

# Initialize the agent with Composio tools
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function to get response using Composio's Perplexity AI Search
def get_composio_perplexity_response(query):
    response = agent.run(query)
    return response

if __name__ == "__main__":
    while True:
        user_query = input("\nEnter your query (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        result = get_composio_perplexity_response(user_query)
        if result:
            print("\nResponse:")
            print(result)
        else:
            print("Failed to get a response.")