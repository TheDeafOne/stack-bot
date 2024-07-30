import pandas as pd
import requests
from bs4 import BeautifulSoup

PAGE_SIZE = 50
STACK_OVERFLOW_URL = 'https://stackoverflow.com/'
QUESTION_HEADER_CLASS = 'h3.s-post-summary--content-title'

def so_url(page, page_size):
    return f'{STACK_OVERFLOW_URL}/questions?tab=newest&page={page}&pagesize={page_size}'

def get_question_urls(page):
    url = so_url(page, PAGE_SIZE)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    question_urls = [STACK_OVERFLOW_URL + question_header['href'] for question_header in soup.select(f'{QUESTION_HEADER_CLASS} > a')]
    return question_urls

# def get_question_question_details


if __name__ == '__main__':
    questions = get_question_urls(1)
    print(questions, len(questions))