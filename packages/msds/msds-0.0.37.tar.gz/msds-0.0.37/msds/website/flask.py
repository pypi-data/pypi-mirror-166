from flask import Flask
from msds.website import routes

def create_app(test_config = None):
    app = Flask(
        __name__,
        instance_relative_config = True,
        template_folder = './view/templates',
        static_folder = './view/static'
    )
    app.config.from_mapping(
        SECRET_KEY = 'random_string'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    routes.init_app(app)

    return app
