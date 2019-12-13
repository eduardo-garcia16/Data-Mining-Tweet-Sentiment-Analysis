import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        consumer_key = '1'
        consumer_secret = '2'
        access_token = '3'
        access_secret = '4'
        # These values are unique and must also never be shared, so please reach out to me if you'd like to run the program with my Twitter Develop Credentials

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    def get_tweets(self, query, count = 1000):
        tweets = []

        try:
            fetched_tweets = self.api.search(q = query, count = count, tweet_mode = 'extended')

            for tweet in fetched_tweets:
                parsed_tweet = {}

                if 'retweeted_status' in tweet._json:
                    parsed_tweet['text'] = tweet._json['retweeted_status']['full_text']
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet._json['retweeted_status']['full_text'])
                else:
                    parsed_tweet['text'] = tweet.full_text
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)


                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))

def main():
    api = TwitterClient()
    tweets = api.get_tweets(query = '@BernieSanders', count = 1000)
    data = open("tweets.txt", "w", encoding="utf-8")

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    data.write("Positive tweets: {}%".format(100*len(ptweets)/len(tweets)) + '\n')

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    data.write("Negative tweets: {}%".format(100*len(ntweets)/len(tweets)) + '\n')


    data.write("\n\n====================\nPositive Tweets:\n")
    for tweet in ptweets[:1000]:
        data.write(tweet['text'] + "\n===\n")

    data.write("\n\n====================\nNegative Tweets:\n")
    for tweet in ntweets[:1000]:
        data.write(tweet['text'] + "\n===\n")

    data.close()

if __name__ == "__main__":
    main()
