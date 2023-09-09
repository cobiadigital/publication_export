from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import keyring
import os

db = SQLAlchemy()



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=keyring.get_password('publication', 'SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
        SQLALCHEMY_BINDS={'project': 'sqlite:///project.db'},
    )

    #app.config['REDIS_URL'] = 'redis://redis:6379'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)



    from . import pubs
    app.register_blueprint(pubs.bp)
    app.add_url_rule('/', endpoint='index')

    @app.cli.command("initdb")
    def initdb():
        """Initializes the database."""
       # db.drop_all()  # Drop all tables
        db.create_all()
        print("Database initialized!")
    return app