from models import  MarketAnalysis, NewsArticles
from settings import get_symbols, get_forecast_period, get_timeframes_in_use, training_data_source, prediction_data_source, use_closing_prices_only, get_model_bidirectional_status,  get_training_logs_path, get_scalers_path, get_models_path, get_models_checkpoints_path, get_error_logs_path, get_natural_language_model_choice
from datetime import datetime
# from database import init_db
from GoogleNews import GoogleNews
import requests
from bs4 import BeautifulSoup
from huggingchat import query_huggingchat_ai
import re
import textwrap

# initialize module's connection to the db
# init_db()

# get news
def get_news(symbol):

    while True:
        # initiate GoogleNews object
        googlenews = GoogleNews()
        # search for news
        googlenews.search(symbol)
        news = googlenews.result()
        print(news)
        # clear object
        googlenews.clear()

        # stop loop if articles are returned
        if len(news) != 0:
            break

    # get current datetime
    current_datetime = str(datetime.now())

    # save articles to database
    # for article in news:
    #     news_details = NewsArticles(
    #         date_released = str(article['datetime']),
    #         asset = symbol,
    #         source = article['media'],
    #         url = article['link'],
    #         title = article['title'],
    #         date_acquired = current_datetime
    #     )
    #     news_details.save()

    # get full articles
    for i in range(len(news)):
        # get article
        article = news[i]

        # URL of the webpage to retrieve
        url = article['link']

        # send a GET request to the URL
        while True:
            try:
                print('Retrieving data from', url, '...')
                response = requests.get(url)
                break
            except:
                print('Error while trying to load', url, '. Retrying...')

        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the readable components of the webpage and store them in a variable
        article_content = soup.find_all('p')  # find all paragraphs ... no specific tags to use since we are not dealing with 1 site with tags we know
        article_text = ''
        for paragraph in article_content:
            paragraph_text = paragraph.get_text()
            # Removing excessive empty lines from full_article using regular expressions
            lines = paragraph_text.splitlines()
            lines = [line for line in lines if line and not line.isspace()]
            paragraph_text = '\n'.join(lines)
            # add paragraph text to article text
            article_text = article_text + '\n\n' + paragraph_text
        print(article_text, '\n\n')

        # add the full article to list
        news[i]['full_article'] = article_text

    # create prompt to feed to the nlp ai model using the news articles
    prompt = ""
    # add full articles to prompt
    for i in range(len(news)):
        article = news[i]
        title = article['title']
        full_article = article['full_article']
        url = article['link']
        prompt = prompt + f""""

******************Article {i+1}*********************
{title}

{full_article}

{url}
****************End of Article {i+1}*****************

        """
    prompt = prompt + f"""

Based only on the articles stated above:
What is your take on what is happening with {symbol}?
What can we expect for {symbol} in the short-term?
What can we expect for {symbol} in the medium term?
What can we expect for {symbol} in the long term?
What should we look out for on {symbol}?
Do not mention any upcoming events unless they have been explicitly stated in the articles given.
Your answers should only be concerned with {symbol} and no other unrelated symbol, asset, or currency pair.
Do not repeat the given questions.
Do not give any other text other than the required answers.
    """
    # query ai and get overview ... according to selected model ... huggingchat /..
    print(prompt)
    overview = ''
    natural_language_model_choice = get_natural_language_model_choice()
    if natural_language_model_choice == 'huggingchat':
        overview = query_huggingchat_ai(
            prompt, 
            True, # create new conversation? ... bool
            False # show conversation list ... bool
        )


    print(overview)




# get list of symbols
symbols = get_symbols()
symbols = ['EURUSD'] # for testing

# get news for each symbol
for symbol in symbols:
    get_news(symbol)