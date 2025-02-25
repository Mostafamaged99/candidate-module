from flask import Flask
from app.config import DevelopmentConfig
import app.models as models
# from app.routes.candidates import candidates_api


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    models.db.init_app(app)
    # app.register_blueprint(candidates_api)
    return app
