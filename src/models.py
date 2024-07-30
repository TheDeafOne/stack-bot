from dataclasses import dataclass


@dataclass
class Post:
    html: str
    post_date: str
    modified_date: str
    votes: int
    comments: list[str]

@dataclass
class Answer(Post):
    accepted: bool


@dataclass
class Question(Post):
    url: str
    title: str
    view_count: int
    answers: int
