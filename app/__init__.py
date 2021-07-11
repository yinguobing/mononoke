from flask import Flask


def create_app(test_config=None):
    """Create and config the app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_ADD="localhost",
        DATABASE_PORT=27017,
        DATABASE_USERNAME="mongoadmin",
        DATABASE_PASSWORD='secret',
        DATABASE_AUTHSOURCE='admin')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    return app
