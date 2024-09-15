import sys, json, os
import modal
import asyncio
from modal import web_endpoint
from hello_world_agent.agent import run_agent as run_hello_world_agent
from run_agents import run_agents_with_topic, groundedness_check
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

    return await run_agents_with_topic(topic)



@app.function()
@web_endpoint(method="GET")
async def web_groundedness_check(topic: str, generated_content: str):

    response = await groundedness_check(topic, generated_content)

    return response

