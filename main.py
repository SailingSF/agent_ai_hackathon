from agents import Agent

def test_agent_run():

    system_prompt = "You are a test agent"
    model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    agent = Agent(system_prompt, model)

    prompt = "Tell me a joke"
    response = agent.submit_message(prompt)

    print(response)

def main():
    test_agent_run()


if __name__ == "__main__":
    
    main()