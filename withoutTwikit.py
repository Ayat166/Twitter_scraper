import requests
from bs4 import BeautifulSoup
import schedule # type: ignore
import time

def parse_and_scrape_profile_tweets(profilename): # parse and scrape profile tweets from accounts
    url = f"{profilename}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    tweets_to_store = []
    for tweet in tweets:
        tweet_text = tweet.find('div', {'lang': True}).get_text()
        tweets_to_store.append({'full_text': tweet_text})
    
    return tweets_to_store


def scrape_twitter(twitter_accounts, ticker, interval): #scrape twitter text to calc the mentions
    mentions = 0
    for account in twitter_accounts:
        tweets = parse_and_scrape_profile_tweets(account)
        mentions += sum(tweet['full_text'].count(ticker) for tweet in tweets)
    
    print(f'"{ticker}" was mentioned "{mentions}" times in the last "{interval}" minutes.')


def schedule_scraping(twitter_accounts, ticker, interval):   #schedule to track each profile in selected time
    schedule.every(interval).minutes.do(scrape_twitter, twitter_accounts, ticker, interval)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

twitter_accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]
ticker = "$TSLA"
interval = 1  # in minutes

schedule_scraping(twitter_accounts, ticker, interval)