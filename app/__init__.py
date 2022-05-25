from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config

# create and configure the app
app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# from app import view, models





# from app import models_new

# from app.main.login import blueprint as login_Blueprint

# app.register_blueprint(blueprint=login_Blueprint)

# login_manager = LoginManager(app, app.context_processor)  
# login_manager.blueprint_login_views = { 
#         'student':  "student.student_login", 
#         'teacher': "teacher.teacher_login",
#         'admin': "admin.admin_login",} 
# admin_app = Blueprint('admin', __name__, url_prefix="/admin")
# teacher_app = Blueprint('teacher', __name__, url_prefix="/teacher_index")
# student_app = Blueprint('student', __name__, url_prefix="/student_index")
# app.register_blueprint(admin_app)
# app.register_blueprint(teacher_app)
# app.register_blueprint(student_app)
# login_manager.login_view = 'login'


