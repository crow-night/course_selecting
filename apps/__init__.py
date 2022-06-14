from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.base import create_app

app = create_app()
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# from apps import models
