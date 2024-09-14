import sys

from hello_world_agent.agent import run_agent

agents_info = {
    "hello_world_agent": {
        "name": "Hello World Agent",
        "description": "An agent that returns a simple greeting.",
    }
}


if len(sys.argv) > 1:
    agent_name = sys.argv[1]
    if agent_name == "hello_world_agent":
        result = run_agent(agent_name)
        print(result)
    else:
        print(
            f"Agent '{agent_name}' does not exist. Options are:\n"
            + "\n".join(
                [f"- {key}: {info['description']}" for key, info in agents_info.items()]
            )
        )

else:
    print("Please provide an agent name as a command line argument.")
