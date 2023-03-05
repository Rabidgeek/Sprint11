from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():
    app = Flask(__name__)

    # Database configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Register our database with the app
    DB.init_app(app)
    my_var = "Twit App"

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='HomePage', users=users)

    @app.route('/bananas')
    def bananas():
        return render_template('base.html', title='Bananas, man...')
    
    @app.route('/reset')
    def reset():
        # Drop all database tables
        DB.drop_all()
        # Recreate all database tables according to the
        # indicated schema in models.py
        DB.create_all()
        return "Database has been reset, dude..."
    
    @app.route('/populate')
    def populate():
        # Create 2 fake users
        jesse = User(id=1, username='Jesse')
        DB.session.add(jesse)
        dave = User(id=2, username='Dave')
        DB.session.add(dave)

        # Create 2 fake tweets
        tweet1 = Tweet(id=1, text='fi fo fe dum I am hungry and gonna eat you', user=jesse)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text='42, the answer to life, the universe, everything.', user=dave)
        DB.session.add(tweet2)

        DB.session.commit()

        return "Database has been populated, bruh"

    return app