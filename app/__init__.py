from flask import Flask
from app.config import DevelopmentConfig
import app.models as models


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    models.db.init_app(app)
    return app
