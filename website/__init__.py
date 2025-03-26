from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# setup a new database
db = SQLAlchemy()
# setup db name
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    #encrypt secure data
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # import views and auth
    from .views import views
    from .auth import auth

    #register our blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # teling flash we are using this db and using sql lite
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}'
    db.init_app(app)

    # make sure that user and note classes are define before we initialise the db
    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    # if db path not exists then create db
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')