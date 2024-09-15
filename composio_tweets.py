

'''
 Python code for the Agent
 with Langchain framework. To get more info,
 see https://docs.composio.dev/
'''
import os
import yaml
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from composio_langchain import ComposioToolSet

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Initialize the toolset
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

# Load configuration from YAML file
config_path = os.path.join(os.path.dirname(__file__), "../config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

pr_review_prompt = config["prompts"]["pr_review_agent"]
pr_summary_prompt = config["prompts"]["pr_summary_agent"]

def main(inputs):
    # Get entity information
    entity = toolset.client.get_entity(inputs["entityId"])

    # Get actions for PR review and summary
    pr_review_tools = toolset.get_actions(
        actions=["github_get_code_changes_in_pr", "github_pulls_create_review_comment"],
        entity_id=entity.id
    )

    pr_summary_tools = toolset.get_actions(
        actions=["github_get_code_changes_in_pr", "github_issues_create_comment"],
        entity_id=entity.id
    )

    # Create agents for code review and PR summary
    code_reviewer_agent = create_tool_calling_agent(
        llm=llm,
        tools=pr_review_tools,
        prompt=ChatPromptTemplate.from_messages([
            ("system", pr_review_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]),
    )

    pr_summariser_agent = create_tool_calling_agent(
        llm=llm,
        tools=pr_summary_tools,
        prompt=ChatPromptTemplate.from_messages([
            ("system", pr_summary_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]),
    )

    # Create executors for the agents
    code_reviewer_executor = AgentExecutor(
        agent=code_reviewer_agent,
        tools=pr_review_tools,
        verbose=True
    )

    pr_summariser_executor = AgentExecutor(
        agent=pr_summariser_agent,
        tools=pr_summary_tools,
        verbose=True
    )

    # Invoke the code reviewer executor
    review_result = code_reviewer_executor.invoke({
        "input": (
            f"Review the provided PR and create review comments if there is any serious issue with the changes. "
            f"Ensure the comment on review PR is posted successfully if an actual comment isn't needed, just ignore it. "
            f"USE github_pulls_create_review_comment to COMMENT ON THE CHANGES. DO NOT COMMENT UNCESSARILY IF THERE IS NO SERIOUS ISSUE OR A TYPO. "
            f"THE URL OF THE PR is: {inputs['PR_URL']}"
        )
    })
    print(review_result)

    # Invoke the PR summariser executor
    summary_result = pr_summariser_executor.invoke({
        "input": (
            f"Summarize the provided PR and post a comment in the GitHub PR with the changes summary. "
            f"Ensure the summary is posted successfully before completing the task using the github_issues_create_comment tool. "
            f"THE URL OF THE PR is: {inputs['PR_URL']}\n"
            f"EXPECTED OUTCOME: A GitHub comment is posted with the changes summary in the specified PR using the github_issues_create_comment tool.\n"
        )
    })
    return summary_result.get("output")

if __name__ == "__main__":
    inputs = {
        "entityId": "user",
        "PR_URL": "https://github.com/composio-ai/playground-agent/pull/1"
    }
    main(inputs)