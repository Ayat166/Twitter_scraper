from twikit import Client # type: ignore
import pandas as pd
import schedule # type: ignore
import time

def parse_and_scrape_profile_tweets(client, username): # parse and scrape profile tweets from accounts
    user = client.get_user_by_screen_name(username)
    tweets = user.get_tweets('Tweets')  
    tweets_to_store = []
    for tweet in tweets:
        tweets_to_store.append({'full_text': tweet.full_text,})
    
    return tweets_to_store


def scrape_twitter(client, twitter_accounts, ticker, interval):  #scrape twitter text to calc the mentions
    mentions = 0
    for account in twitter_accounts:
        tweets = parse_and_scrape_profile_tweets(client, account)
        mentions += sum(tweet['full_text'].count(ticker) for tweet in tweets)
    
    print(f'"{ticker}" was mentioned "{mentions}" times in the last "{interval}" minutes.')

def schedule_scraping(client, twitter_accounts, ticker, interval):  #schedule to track each profile in selected time
    schedule.every(interval).minutes.do(scrape_twitter, client, twitter_accounts, ticker, interval)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


client = Client('en-US')

# Login and save cookies
client.login(
    auth_info_1='UserName',
    password='Password',
)
client.save_cookies('cookies.json')
client.load_cookies(path='cookies.json')

twitter_accounts = [
    "Mr_Derivatives",
    "warrior_0719",
    "ChartingProdigy",
    "allstarcharts",
    "yuriymatso",
    "TriggerTrades",
    "AdamMancini4",
    "CordovaTrades",
    "Barchart",
    "RoyLMattox"
]
ticker = "$TSLA"
interval = 1  # in minutes

schedule_scraping(client, twitter_accounts, ticker, interval)

# not that i make the interval one minute you can increase it as you want
# I make the interrupt to stop the run time it's not error 
# the reason of getting 0 in the first code is because of twitter require signin to access the data so that i used Twikit 
# Thank you 