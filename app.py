from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from db import db

from resources.versions import blp as VersionsBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "LOL Static Data REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["MONGO_URI"] = f"mongodb+srv://{environ.get('DB_USERNAME')}:" \
                              f"{environ.get('DB_PASSWORD')}@" \
                              f"{environ.get('DB_CLUSTER')}/" \
                              f"{environ.get('DB_NAME')}"

    db.init_app(app)
    api = Api(app)

    api.register_blueprint(VersionsBlueprint)

    return app
