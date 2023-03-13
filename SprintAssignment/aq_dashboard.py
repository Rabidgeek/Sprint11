"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .openaq import OpenAQ

def create_app():
    app = Flask(__name__) 

    # Database Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    DB = SQLAlchemy(app)

    api = OpenAQ()

    # Functions
    def get_results():
        try:
            status, body = api.measurements(city='Los Angeles', parameter='pm25') 
            if status != 200:
                raise Exception(f'Data Retrival Failure!!! Status: {status}')
            results = [(r['date']['utc'], r['value']) for r in body['results']]

            return results
        except Exception as e:
            print(f'ZOMG We got an issue here: \n{e}\n')
            return []
    
    # Routing
    @app.route('/')
    def root():
        results = get_results()
        response = "<ul>"
        for result in results:
            item = f"<li>UTC Time: {result[0]}, PM25 Value: {result[1]} </li>"
            response += item
        return response

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        results = get_results()
        for result in results:
            record = Record(datetime=result[0], value=result[1])
            DB.session.add(record)
        DB.session.commit()
        return 'Data refreshed!'
    
    class Record(DB.Model):
        # id (integer, primary key)
        id = DB.Column(DB.Integer, primary_key=True)
        # datetime (string)
        datetime = DB.Column(DB.String(25))
        # value (float, cannot be null)
        value = DB.Column(DB.Float, nullable=False)

        def __repr__(self):
            return f'< UTC Time: {self.datetime} --- Value: {self.value}'


    return app

