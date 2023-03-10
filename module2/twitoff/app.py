from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user

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
    
    @app.route('/populate')
    def populate():
        # Create 2 fake users
        add_or_update_user('austen')
        add_or_update_user('nasa')
        add_or_update_user('jesseragsdale')

        return render_template('base.html', title='DB has been populated, bruh')
    
    @app.route('/update')
    def update():
        # get a list of usernames of all users
        users = Users.query.all()
        usernames = []
        #for user in users:
        #    usernames.append(user.username)
        # list comprehension version
        for username in [user.username for user in users]:
            add_or_update_user(username)

    return app