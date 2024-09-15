import modal
import sys, json, os
from news_agent.agent import NewsAgent
from useful_facts_agent.agent import UsefulFactsAgent
from hello_world_agent.agent import HelloWorldAgent
from tweet_agent.agent import TweetAgent


import asyncio
from modal import web_endpoint, Image

from run_agents import run_agents_with_topic, groundedness_check

app = modal.App("social-swarm")
image = Image.debian_slim(python_version="3.10").pip_install(
    "datasets",
    "python-dotenv",
    "openai",
    "together",
    "pydantic>=2.0",
    "fastapi>=0.100",
)


@app.function(image=image)
@web_endpoint(method="GET")
async def hello_world_agent(subject: str):
    return HelloWorldAgent.run(subject)


@app.function(image=image, secrets=[modal.Secret.from_name("my-custom-secret")])
@web_endpoint(method="GET")
async def useful_facts_agent(subject: str):
    return UsefulFactsAgent.run_agent(subject)


@app.function(image=image, secrets=[modal.Secret.from_name("my-custom-secret")])
@web_endpoint(method="GET")
async def news_agent(subject: str):
    return NewsAgent.run_agent(subject)


@app.function(image=image, secrets=[modal.Secret.from_name("my-custom-secret")])
@web_endpoint(method="GET")
async def get_validated_tweets(topic: str) -> str:
    """
    A single function to generate tweets that are generated with agents
    The tweets then pass a groundedness check for validation
    Text is returned
    """

    return await run_agents_with_topic(topic)


@app.function()
@web_endpoint(method="GET")
async def web_groundedness_check(topic: str, generated_content: str):

    response = await groundedness_check(topic, generated_content)

    return response

@app.function()
@web_endpoint(method="GET")
async def send_tweet(tweet: str):

    return TweetAgent.run_agent(tweet)