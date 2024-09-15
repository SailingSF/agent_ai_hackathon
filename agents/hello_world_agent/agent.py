from classes import Tweet


class HelloWorldAgent:
    def run(self, subject: str) -> list[Tweet]:
        return [Tweet(text=f"{subject} are taking over the world!")]
