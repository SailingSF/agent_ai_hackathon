from dataclasses import dataclass


@dataclass
class Tweet:
    text: str
    link_url: str = None
    image_url: str = None
