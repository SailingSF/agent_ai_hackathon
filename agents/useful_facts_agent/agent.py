from tools.together_tools import query_together
from classes import Tweet


class UsefulFactsAgent:
    def run_agent(subject: str) -> list[Tweet]:
        response = query_together(
            f"Generate 3 tweets with fun facts about {subject}. Your response should not contain any other text than the 3 tweets, one per line."
        )
        content = response.choices[0].message.content
        tweets = [Tweet(text=line.strip()) for line in content.split("\n\n")]
        return tweets
