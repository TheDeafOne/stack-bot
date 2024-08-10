from flask import Flask, render_template

from scraper.scraper import get_questions_on_page

app = Flask(__name__)
questions = get_questions_on_page(1)

@app.route("/")
def index():

    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run()