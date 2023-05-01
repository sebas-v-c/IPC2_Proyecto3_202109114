import os

from flask import Flask

from .api.api import configure_api
from .data.db import init_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "DB", "db.xml"),
        ALLOWED_EXTENSIONS=["xml"],
        UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads"),
    )

    app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(os.path.join(app.instance_path, "DB"))
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, "uploads"))
    except OSError:
        pass

    init_db(app)
    configure_api(app)

    @app.route("/api")
    def up():
        return "Hello, World!"

    return app
