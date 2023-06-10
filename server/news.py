from models import  MarketAnalysis, NewsArticles
from settings import get_symbols, get_forecast_period, get_timeframes_in_use, training_data_source, prediction_data_source, use_closing_prices_only, get_model_bidirectional_status,  get_training_logs_path, get_scalers_path, get_models_path, get_models_checkpoints_path, get_error_logs_path, get_natural_language_model_choice
from datetime import datetime
# from database import init_db
from GoogleNews import GoogleNews
import requests
from bs4 import BeautifulSoup
from huggingchat import query_huggingchat_ai
import re

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
        # print(news)
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
        response = requests.get(url)

        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the readable components of the webpage and store them in a variable
        article_content = soup.find('body')  # using body to try and cover everything on all sites because sites use different tags for their articles
        article_text = article_content.get_text()
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
        # Removing excessive empty lines from full_article using regular expressions
        lines = full_article.splitlines()
        lines = [line for line in lines if line and not line.isspace()]
        full_article = '\n'.join(lines)
        url = article['link']
        prompt = prompt + f""""

        ******************Article {i+1}*********************
        {title}

        {full_article}

        {url}
        ****************End of Article {i+1}*****************

        """
    prompt = prompt + f"""


    Given the articles listed above, give an overview on what is happening with {symbol} according to your own analysis.
    Give a straight answer, do not repeat the scenario / question, do not give any other speech / text other than the answer, no formalities.
    """
    # query ai and get overview ... according to selected model ... huggingchat /..
    print(prompt)
    overview = ''
    natural_language_model_choice = get_natural_language_model_choice()
    if natural_language_model_choice == 'huggingchat':
        overview = query_huggingchat_ai(prompt)

    print(overview)




# get list of symbols
symbols = get_symbols()
symbols = ['EURUSD'] # for testing

# get news for each symbol
for symbol in symbols:
    get_news(symbol)