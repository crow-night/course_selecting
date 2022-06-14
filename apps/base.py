import os

from flask import Flask

from apps.configs import Config

static_path = os.path.join(os.path.dirname(__file__), 'static')


def create_app():
    config = Config
    app = Flask(config.SERVICE_NAME, static_folder=static_path)
    app.config.from_object(config)

    return app


def add_blueprint(app, blueprints):
    # 导入蓝图
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
