from flask import Flask
from app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    return app

