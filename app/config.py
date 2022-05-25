import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/course_select?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
