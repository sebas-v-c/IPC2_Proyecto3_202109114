import functools


from .reset import reset_bp
from .users.users import users
from .messages.messages import messages


def configure_api(app):
    # add blueprints
    app.register_blueprint(reset_bp, url_prefix="/api")
    app.register_blueprint(users, url_prefix="/api")
    app.register_blueprint(messages, url_prefix="/api")
