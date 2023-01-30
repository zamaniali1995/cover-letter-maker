"""Flask run file."""
from flask import Flask, render_template, request

from src.utils import make_cover_letter_with_chatgpt, parse_cv, parse_html_page

app = Flask(__name__)


@app.route('/')
def index():
    """Index function."""
    return render_template('index.html')


@app.route('/make', methods=['POST'])
def make_cover_letter():
    """
    Make cover letter.

    Get resume and url of job posting website.
    Extract text from them.
    build a cover letter with ChatGPT based on extracted text.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    text_cv = ''
    if request.files['cv'] != '':
        text_cv = parse_cv(file=request.files['cv'])

    access_token = request.form.get('access-token')
    text_html = parse_html_page(url=request.form.get('url'))
    text = text_cv + text_html
    print(text)
    cover_letter = make_cover_letter_with_chatgpt(
        info=text, access_token=access_token)
    return render_template('index.html', resp=cover_letter)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='300', debug=True)
