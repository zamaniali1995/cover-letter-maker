"""Utils file."""
import asyncio
from typing import Text
from urllib.request import urlopen

from bs4 import BeautifulSoup
from ChatGPT_lite.ChatGPT import Chatbot
from PyPDF2 import PdfReader


def parse_cv(file) -> Text:
    """
    Parse resume.

    Parameters
    ----------
    file: Object
        File of Resume

    Returns
    -------
    Text
        Parsed text from resume
    """
    text = ''
    try:
        reader = PdfReader(file)
        for i in range(len(reader.pages)):
            text += reader.pages[i].extract_text()
        text = process_text(text=text)
    except:
        text = ''
    return text


def parse_html_page(url: Text) -> Text:
    """
    Parse a website.

    Parameters
    ----------
    url: Text
        Url of the website

    Returns
    -------
    Text
        Parsed text from the website
    """
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features='html.parser')
    text = soup.get_text()
    text = process_text(text=text)
    return text


def process_text(text: Text) -> Text:
    """
    Process text.

    Parameters
    ----------
    text: Text
        Text to process

    Returns
    -------
    Text
        Process text
    """
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
    # drop blank lines
    processed_text = ' '.join(chunk for chunk in chunks if chunk)
    processed_text = ' '.join(processed_text.split(' ')[:800])
    return processed_text


def make_cover_letter_with_chatgpt(info: Text, access_token: Text) -> Text:
    """
    Make cover letter according to the info with ChatGPT.

    Parameters
    ----------
    info: Text
        Extracted info from resume and job posting website

    access_token: Text
        Access token from https://chat.openai.com/chat website
        Login to the website -> Right click on the page ->
        Click on Inspect -> Go to Application tab
        Find Cookies -> Find __Secure-next-auth.session-token

        Or

        Install ChatGPT Cookies extension on Chrome ->
        Go to https://chat.openai.com/chat -> Click on the extension ->
        Click on "Copy Session Token"

    Returns
    -------
    Text
        Generated cover letter
    """
    chat = Chatbot(access_token)
    # Create loop
    loop = asyncio.new_event_loop()
    # Set
    asyncio.set_event_loop(loop)
    # Run
    loop.run_until_complete(chat.wait_for_ready())
    while True:
        try:
            response = loop.run_until_complete(
                chat.ask(
                    'write a cover letter with the following information: ' + info)
            )
            cover_letter = response['answer']
            cover_letter = cover_letter.split('\n')
            if '' in cover_letter:
                cover_letter.remove('')
            if response['answer'] != 'Bot: Error occurred':
                break
        except KeyboardInterrupt:
            break
    # Close sockets
    chat.close()
    # stop asyncio event loop
    loop.stop()
    return cover_letter
