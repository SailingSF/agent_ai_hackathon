from dataclasses import dataclass


@dataclass
class Tweet:
    text: str
    image_url: str = None


def run_agent(subject: str) -> Tweet:
    return [Tweet(text="hi")]


print(run_agent("Rabbits"))
