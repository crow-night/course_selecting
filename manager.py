from werkzeug.middleware.proxy_fix import ProxyFix

from apps import app
from apps.admin import blueprint as admin
from apps.base import add_blueprint
from apps.login import blueprint as login
from apps.student import blueprint as student
from apps.teacher import blueprint as teacher

blueprints = [login, admin, student, teacher]

if __name__ == '__main__':

    app = add_blueprint(app, blueprints)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(port="8000", debug=True)
