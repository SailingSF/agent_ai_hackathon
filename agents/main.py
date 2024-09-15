import sys, json, os
from typing import List, Dict
from tools.perplexity_news import get_perplexity_response
from openai import OpenAI
from agent_class import Agent
from dotenv import load_dotenv
import modal
import asyncio
from modal import web_endpoint
from hello_world_agent.agent import run_agent as run_hello_world_agent
import logging
logger = logging.getLogger(__name__)
load_dotenv()

app = modal.App("social-swarm")


@app.function()
@web_endpoint(method="GET")
async def hello_world_agent(subject: str):
    return run_hello_world_agent(subject)

@app.function()
@web_endpoint(method="GET")
async def get_validated_tweets(topic: str) -> str:
    '''
    A single function to generate tweets that are generated with agents
    The tweets then pass a groundedness check for validation
    Text is returned
    '''

    return asyncio.run(main())

def get_tweets(query: str):

    return "Tweets"

def groundedness_check(topic: str, generated_content: str):

    api_key = os.environ.get("UPSTAGE_API_KEY")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    response = client.chat.completions.create(
        model="solar-1-mini-groundedness-check",
        messages=[
            {"role": "user", "content": f"Generate tweets for the topic of {topic} after gathering interesting facts and context"},
            {"role": "assistant", "content": generated_content}
        ]
    )

    return response


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
    logging.basicConfig(level=logging.INFO)

    main_model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    small_model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    with open('tools.json', 'r') as file:
        tools_data = json.load(file)
        tool_definitions = tools_data['tools']

    news_agent = Agent(
        name="News agent",
        system_prompt="You are a news retriever. Find recent news about the given topic.",
        model=main_model,
        tools=tool_definitions,
        tools_map={"get_news": get_perplexity_response}
    )
    
    social_media_agent = Agent(
        name="Social Media Agent",
        system_prompt="You are a social media analyzer. Analyze social media trends for the given topic and use your tool to see posts from X/Twitter.",
        model="your_chosen_model",
        tools=[{"function": {"name": "analyze_social_media", "description": "Analyze social media trends"}}],
        tools_map={"retrieve_tweets": get_tweets}
    )
    
    tweet_generator_agent = Agent(
        name="Tweet generator agent",
        system_prompt="You are a tweet generator. Create engaging tweets based on the given topic and context.",
        model=main_model
    )
    
    agents = {
        'news_retriever': news_agent,
        'tweet_generator': tweet_generator_agent
    }
    topic="The health of rabits"
    tweets = await orchestrate_tweet_generation(topic, agents)
    print(tweets)
    groundedness = groundedness_check(topic, str(tweets))

if __name__ == "__main__":
    asyncio.run(main())