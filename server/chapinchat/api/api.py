import functools


from .reset import reset_bp


def configure_api(app):
    # add blueprints
    app.register_blueprint(reset_bp, url_prefix="/api")
    pass
