from flask import Flask  # import the Flask class from flask module
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()  # Initializing SQLAlchemy claas
DB_NAME = 'database.db'
mail = Mail() # Initializing Mail class


def create_app(config_name):  # a method to instantiate our App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)  # initialise our db
    mail.init_app(app) # initialize our mail
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    bootstrap = Bootstrap(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # importing our blueprints
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    # Registering our blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/')

    # import our db object classes
    from .models import User, Pitch

    # call the method to craete our db
    create_database(app)

    return app


# create our db
def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Database has been created')