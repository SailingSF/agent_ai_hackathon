import asyncio
from agent_class import Agent
import json
from typing import List, Dict
from agents.tools.perplexity_news import get_perplexity_response

def get_tweets(query: str):

    return "Tweets"

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

async def orchestrate_tweet_generation(topic: str, agents: Dict[str, Agent]) -> List[str]:
    """
    Orchestrate the process of gathering information and generating tweets using custom Agent instances.
    
    :param topic: The topic to generate tweets about
    :param agents: A dictionary of Agent instances, keyed by their role
    :return: A list of generated tweets
    """
    # Step 1: Gather information
    context = await gather_information(topic, agents)
    
    # Step 2: Generate tweets
    tweets = await generate_tweets(topic, context, agents)
    
    return tweets

async def gather_information(topic: str, agents: Dict[str, Agent]) -> str:
    """
    Use various agents to gather information about the topic.
    """
    tasks = []
    
    for role, agent in agents.items():
        if role != 'tweet_generator':
            tasks.append(asyncio.to_thread(agent.submit_message, f"Gather information about {topic}"))
    
    results = await asyncio.gather(*tasks)
    
    return ' '.join(results)

async def generate_tweets(topic: str, context: str, agents: Dict[str, Agent]) -> List[str]:
    """
    Use the tweet_generator agent to create tweets based on the gathered information.
    """
    if 'tweet_generator' not in agents:
        raise ValueError("Tweet generator agent is required")
    
    prompt = f"Generate engaging tweets about {topic} based on this context: {context}"
    tweets_text = await asyncio.to_thread(agents['tweet_generator'].submit_message, prompt)
    
    # Assuming the tweet_generator returns a string with tweets separated by newlines
    tweets = tweets_text.strip().split('\n')
    return tweets

async def main():
    # Define your agents with appropriate system prompts, models, and tools

    main_model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    small_model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    with open('tools.json', 'r') as file:
        tools_data = json.load(file)
        tool_definitions = tools_data['tools']

    news_agent = Agent(
        system_prompt="You are a news retriever. Find recent news about the given topic.",
        model=main_model,
        tools=tool_definitions,
        tools_map={"get_news": get_perplexity_response}
    )
    
    social_media_agent = Agent(
        system_prompt="You are a social media analyzer. Analyze social media trends for the given topic and use your tool to see posts from X/Twitter.",
        model="your_chosen_model",
        tools=[{"function": {"name": "analyze_social_media", "description": "Analyze social media trends"}}],
        tools_map={"retrieve_tweets": get_tweets}
    )
    
    tweet_generator_agent = Agent(
        system_prompt="You are a tweet generator. Create engaging tweets based on the given topic and context.",
        model=main_model
    )
    
    agents = {
        'news_retriever': news_agent,
        'tweet_generator': tweet_generator_agent
    }
    
    tweets = await orchestrate_tweet_generation("The health of rabbits", agents)
    print(tweets)

if __name__ == "__main__":
    asyncio.run(main())