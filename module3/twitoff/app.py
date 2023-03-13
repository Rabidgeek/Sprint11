from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user


def create_app():
    app = Flask(__name__)

    # Database configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register our database with the app
    DB.init_app(app)

    @app.route('/')
    def root():
        # return page contents
        users = User.query.all()
        return render_template('base.html', title="Home", users=users)

    @app.route('/reset')
    def reset():
        # Drop all database tables
        DB.drop_all()
        # Recreate all database tables according to the
        # indicated schema in models.py
        DB.create_all()
        return render_template('base.html', title='Reset teh DB, d00d')

    @app.route('/update')
    def update():
        # get a list of usernames of all users
        # users = User.query.all()
        usernames = update_all_users()

        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html',
                               title='DB has been populated, bruh')

    @app.route('/iris')
    def iris():
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                                 multi_class='multinomial').fit(X, y)

        return str(clf.predict(X[:2, :]))

    @app.route('/user', methods=["POST"])
    @app.route('/user/<username>', methods=["GET"])
    def user(name=None, message=''):
        username = name or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = 'User "{username}" has been successfully added!'

            tweets = User.query.filter(User.username == username).one()
        except Exception as e:
            message = f'Error adding {username}: Your issue is {e}'
            tweets = []

        return render_template('user.html',
                               title=username,
                               tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'],
                               request.values['user1']])
        hypo_tweet_text = request.values['tweet_text']

        if user0 == user1:
            message = 'Cannae compare user to themself, capt\'n!'
        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)

            # get into the if statement if prediction is user1
            if prediction:
                message = f'''"{hypo_tweet_text}" is more likely something
                               {user1} would tweet, not {user0}'''
            else:
                message = f'''"{hypo_tweet_text}" is more likely something
                               {user0} would tweet, not {user1}'''

        return render_template('prediction.html',
                               title='Prediction',
                               message=message)

    return app
