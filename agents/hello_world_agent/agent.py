from dataclasses import dataclass


@dataclass
class Tweet:
    text: str
    image_url: str = None


def run_agent(subject: str) -> Tweet:
    return [Tweet(text="Rabbits are taking over the world!")]


print(run_agent("Rabbits"))
