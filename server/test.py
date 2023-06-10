from GoogleNews import GoogleNews

def get_news(asset_class):

    while True:
        googlenews = GoogleNews()
        googlenews.search(asset_class)
        news = googlenews.result()
        print(news)
        googlenews.clear()

        if len(news) != 0:
            print(str(news[-1]['datetime']))
            break

    return news

get_news('EURUSD')