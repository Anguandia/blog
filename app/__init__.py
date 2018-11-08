#import required modules
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


#initialise extensions
app=Flask(__name__, instance_relative_config=True)

#load app components
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate=Migrate(app, db)
login=LoginManager(app)
login.login_view='login'

from app import views, models