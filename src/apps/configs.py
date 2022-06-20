import os


class Config:
    """
    config setting
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/course_select?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask setting
    PORT = 8000
    HOST = "0.0.0.0"
    DEBUG = True
    SERVICE_NAME = "course_selecting"
