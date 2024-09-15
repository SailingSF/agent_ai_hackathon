import tweepy
import os
from datetime import datetime, timedelta

class TwitterSearcher:
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def get_recent_tweets(self, topic, max_results=10):
        query = f"{topic} -is:retweet"  # Exclude retweets
        start_time = datetime.now(datetime.timezone.utc) - timedelta(days=7)  # Last 7 days

        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                start_time=start_time
            )

            if not tweets.data:
                print(f"No tweets found for the topic: {topic}")
                return []

            processed_tweets = []
            for tweet in tweets.data:
                processed_tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'metrics': tweet.public_metrics,
                    'author_id': tweet.author_id
                })

            # Sort by engagement (likes + retweets + replies + quote_count)
            sorted_tweets = sorted(
                processed_tweets,
                key=lambda x: sum(x['metrics'].values()),
                reverse=True
            )

            return sorted_tweets[:max_results]

        except tweepy.TweepError as e:
            print(f"An error occurred: {e}")
            return []

    def print_tweets(self, tweets, topic):
        if tweets:
            print(f"Top {len(tweets)} recent tweets about '{topic}':")
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. Tweet ID: {tweet['id']}")
                print(f"   Text: {tweet['text']}")
                print(f"   Created at: {tweet['created_at']}")
                print(f"   Metrics: {tweet['metrics']}")
        else:
            print("No tweets retrieved or an error occurred.")

# Example usage
if __name__ == "__main__":
    # Load API credentials from environment variables
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    # Create an instance of TwitterSearcher
    searcher = TwitterSearcher(api_key, api_secret, access_token, access_token_secret)

    # Search for tweets
    topic = "artificial intelligence"
    max_results = 10
    tweets = searcher.get_recent_tweets(topic, max_results)

    # Print the results
    searcher.print_tweets(tweets, topic)