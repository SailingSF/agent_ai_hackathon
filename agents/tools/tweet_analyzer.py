from tools.together_tools import query_together
from classes import Tweet
import json


class TweetAnalyzer:
    def analyze(tweet: Tweet):
        response = query_together(
            f'For the following tweet, please do a sentiment analysis and reply in this json format {{ "sentiment": "neutral"}}. Do not add any text before or after the json. Tweet: {tweet.text}'
        )
        content = response.choices[0].message.content
        print(content)
        data = json.loads(content)
        return data
