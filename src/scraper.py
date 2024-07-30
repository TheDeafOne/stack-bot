from datetime import datetime

import requests
from bs4 import BeautifulSoup

from models import Answer, Question

PAGE_SIZE = 50
STACK_OVERFLOW_URL = 'https://stackoverflow.com/'
QUESTION_HEADER_CLASS = 'h3.s-post-summary--content-title'
BS_PARSER = 'html.parser'
DATE_FORMAT = '%b %d, %Y at %H:%M'

def so_url(page, page_size):
    return f'{STACK_OVERFLOW_URL}/questions?tab=newest&page={page}&pagesize={page_size}'

def get_question_urls(page):
    url = so_url(page, PAGE_SIZE)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, BS_PARSER)
    question_urls = [STACK_OVERFLOW_URL + question_header['href'] for question_header in soup.select(f'{QUESTION_HEADER_CLASS} > a')]
    return question_urls

def get_comments(soup: BeautifulSoup):
    comments = [
        comment_list_item.select_one('div.comment-text > div > span.comment-copy').text 
        for comment_list_item 
        in soup.select('ul.comments-list > li')
    ]
    return comments

def parse_answer(soup: BeautifulSoup):
    date_info = [info.text for info in soup.select('span.relativetime')]
    post_date = date_info[-1]
    modified_date = date_info[0] if len(date_info) > 1 else post_date
    
    voting_container = soup.select_one('div.js-voting-container')
    vote_count = int(voting_container.select_one('div.js-vote-count').text)
    
    accepted = voting_container.select_one('div.js-accepted-answer-indicator') is not None

    return Answer(
        html=soup,
        post_date=post_date,
        modified_date=modified_date,
        votes=int(vote_count),
        comments=get_comments(soup),
        accepted=accepted
    )

def parse_question(soup: BeautifulSoup):
    answers = list(map(parse_answer, soup.find_all('div', {'class': 'answer'})))
    print(answers[0])
    
        


def get_questions(urls):
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, BS_PARSER)
        parse_question(soup)
        break

    

if __name__ == '__main__':
    questions = get_question_urls(1)
    get_questions(['https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup'])