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
    def __repr__(self):
        return f'{self.__class__.__name__}(post_date={self.post_date}, votes={self.votes}), accepted={self.accepted}'


@dataclass
class Question(Post):
    url: str
    title: str
    view_count: int
    answers: int
