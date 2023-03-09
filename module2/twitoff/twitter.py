from os import getenv
import not_tweepy as tweepy
import spacy
from .models import DB, Tweet, User

# Get out API keys from our .env file
key = getenv('TWITTER_KEY_API')
secret = getenv('TWITTER_KEY_API_SECRET')

# Connect to the twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    '''Take a username and pull that user's data and tweets from the
    API. if this user alredy exists in our database then we will just 
    check to see if there are any new tweets from that uer that we don't
    already have and we will add any new tweets to the DB. '''
    try:
        # Get the user info from twitter
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if this user is already in the database
        # Is there a user with the same id already in the db?
        # If we don't have the user, then create it
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

        # Add the user to the database
        # This wont re-add if they already exist
        DB.session.add(db_user)

        # Get the user's tweets
        tweets = twitter_user.timeline(count=200, 
                                    exclude_replies=True, 
                                    include_rts=False, 
                                    tweet_mode='extended',
                                    since_id=db_user.newest_tweet_id)
        
        # Add all of the individual's tweets to the database
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, 
                            text=tweet.full_text[:300],
                            vect=tweet_vector,
                            user_id=db_user.id)
            DB.session.add(db_tweet)
    except Exception as e:
        print(f'Error Processing {username}: {e}, dude... fix this shit!')
        raise e
    else:
        # Save the changes to the DB
        DB.session.commit()

nlp = spacy.load('my_model/')
# We have the same tool we used in the flask shell here in our file
# give the function some text, it returns a word embedding
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector