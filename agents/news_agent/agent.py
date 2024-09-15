from tools.together_tools import query_together
from classes import Tweet
import json


class NewsAgent:
    def run_agent(subject: str) -> list[Tweet]:
        response = query_together(
            f"find 3 recent news articles about {subject} and create engaging tweets for them. Your whole reply should be a valid json with the format [{{'text': 'tweet text', 'article_url': 'url to the article'}}]. Absolutely no text before or after the json."
        )
        content = response.choices[0].message.content
        tweets_data = json.loads(content)
        tweets = [
            Tweet(text=item["text"], link_url=item["article_url"])
            for item in tweets_data
        ]
        return tweets
