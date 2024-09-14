import sys

import modal
from modal import web_endpoint
from hello_world_agent.agent import run_agent as run_hello_world_agent


app = modal.App("social-swarm")


@app.function()
@web_endpoint(method="GET")
async def hello_world_agent(subject: str):
    return run_hello_world_agent(subject)
