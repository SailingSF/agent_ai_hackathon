from agent_class import Agent
import json
from agents.tools.perplexity_news import get_perplexity_response

def test_agent_run():

    system_prompt = "You are a test agent"
    model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

    with open('tools.json', 'r') as file:
        tools_data = json.load(file)
        tool_definitions = tools_data['tools']

    tool_map = {"get_news": get_perplexity_response}
    agent = Agent(system_prompt, model, tool_definitions, tool_map)
    print(agent)
    prompt = "Tell me about the recent US presidential debate, concisely."
    response = agent.submit_message(prompt)

    print(response)

def main():
    test_agent_run()


if __name__ == "__main__":
    
    main()