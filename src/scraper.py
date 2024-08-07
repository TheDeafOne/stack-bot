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

def get_dates(soup: BeautifulSoup):
    date_info = [info.text for info in soup.select('span.relativetime')]
    post_date = date_info[-1]
    modified_date = date_info[0] if len(date_info) > 1 else post_date
    return post_date, modified_date

def parse_answer(soup: BeautifulSoup):
    post_date, modified_date = get_dates(soup)
    voting_container = soup.select_one('div.js-voting-container')
    vote_count = int(voting_container.select_one('div.js-vote-count').text)
    
    accepted = 'd-none' not in voting_container.select_one('div.js-accepted-answer-indicator')['class']

    return Answer(
        html=soup,
        post_date=post_date,
        modified_date=modified_date,
        votes=vote_count,
        comments=get_comments(soup),
        accepted=accepted
    )


def parse_question(soup: BeautifulSoup, url: str):
    answers = list(map(parse_answer, soup.find_all('div', {'class': 'answer'})))
    question = soup.select_one('div.question')
    post_date, modified_date = get_dates(soup)
    voting_container = question.select_one('div.js-voting-container')
    vote_count = int(voting_container.select_one('div.js-vote-count').text)
    
    title = soup.select_one('a.question-hyperlink').text
    view_count_div = soup.find_all('div', title=lambda title: title and 'viewed' in title.lower())[0]
    view_count = int(view_count_div['title'].split()[1].replace(',', ''))

    return Question(
        html=soup,
        post_date=post_date,
        modified_date=modified_date,
        votes=vote_count,
        comments=get_comments(question),
        url=url,
        title=title,
        view_count=view_count,
        answers=answers
    )
    
        


def get_questions(urls):
    questions = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, BS_PARSER)
        questions.append(parse_question(soup, url))
        break
    return questions

    

if __name__ == '__main__':
    questions = get_questions(['https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup'])
    print(questions)