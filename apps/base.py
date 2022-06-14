from flask import Flask

from apps.configs import Config


def create_app():
    config = Config
    app = Flask(config.SERVICE_NAME, static_url_path='/static')
    app.config.from_object(config)

    return app


def add_blueprint(app, blueprints):
    # 导入蓝图
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
