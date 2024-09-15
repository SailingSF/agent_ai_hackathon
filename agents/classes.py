from dataclasses import dataclass


@dataclass
class Tweet:
    text: str
    image_url: str = None
