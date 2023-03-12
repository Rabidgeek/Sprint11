from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):
    # grab the users from DB
    user0 = User.query.filter(User.username==user0_username)
    user1 = User.query.filter(User.username==user1_username)

    # get the word embeddings from each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    
    # vertically stack the 2 2-d numpy arrays to make our X Matrix
    X_train = np.vstack([user0_vects, user1_vects])

    # concatenate our labels of 0 or 1 for each tweet
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user1_vects.shape[0])

    y_train = np.concatenate([zeros, ones])

    # instantiate and fit a logreg model
    log_reg = LogisticRegression().fit(X_train, y_train)

    # vectorize the hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    return log_reg.predict(hypo_tweet_vect)[0]