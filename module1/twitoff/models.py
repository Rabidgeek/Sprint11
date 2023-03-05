from flask_sqlalchemy import SQLAlchemy

# create a DB Obj from SQLAlchemy class

DB = SQLAlchemy()

class User(DB.Model):
    # ID Col
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Username Col
    username = DB.Column(DB.String, nullable=False)
    # backref is as-f we had added a tweets list to the user class
    # tweets = []

    def __repr__(self):
        return f"User: {self.username}"

class Tweet(DB.Model):
    # ID col
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Text col
    text = DB.Column(DB.Unicode(300))
    # user_id col - foreign/secondary key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # user column creates a two-way link between an user object and a tweet
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"Tweet: {self.text}"
