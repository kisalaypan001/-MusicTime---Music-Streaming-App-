from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

import os


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vulege6i'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    UPLOAD_FOLDER = 'static'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')
    db.init_app(app)






    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
 

    from .models import User


    create_database(app)
    
    login_manager= LoginManager()
    login_manager.login_view = 'auth.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

#Create default admin


from .models import Admin
def create_database(app):
    if not path.exists("websites/instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
        with app.app_context(): #Adding a default admin
            admin = Admin.query.filter_by(email='admin').first()
            if not admin:
                default_admin = Admin(email='admin', password='password')
                db.session.add(default_admin)
                db.session.commit()


