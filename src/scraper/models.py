from dataclasses import dataclass


@dataclass
class Post:
    html: str
    post_date: str
    modified_date: str
    votes: int
    comments: list[str]
    text: str


@dataclass
class Answer(Post):
    accepted: bool
    def __repr__(self):
        return f'{self.__class__.__name__}(post_date={self.post_date}, votes={self.votes}, accepted={self.accepted})'


@dataclass
class Question(Post):
    url: str
    title: str
    view_count: int
    answers: int

    def __repr__(self):
        return f'{self.__class__.__name__}(title="{self.title}", post_date={self.post_date}, votes={self.votes}, view_count={self.view_count})'

@dataclass
class QuestionSummary:
    title: str
    post_date: str
    view_count: int
    url: str
    text: str
    answer_count: int
    vote_count: int

    def __repr__(self):
        return f'{self.__class__.__name__}(title="{self.title}", post_date={self.post_date}, view_count={self.view_count}, answer_count={self.answer_count}, vote_count={self.vote_count})'