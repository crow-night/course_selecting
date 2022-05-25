import os
from flask import Blueprint
from flask.views import MethodViewType
from functools import wraps


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/course_select?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

# def class_route(blueprint: Blueprint, rule, **options):
#     """class view 的路由"""

#     def decorator(view):
#         if isinstance(view, MethodViewType):
#             view_func = view.as_view(view.__name__)
#         else:
#             view_func = view

#         blueprint.add_url_rule(
#             rule, view.__name__, view_func=view_func, **options
#         )
#         return view

#     return decorator

# def route(blueprint: Blueprint, rule, **options):
#     """函数 view 的路由"""

#     def wrapper(view):

#         @wraps(view)
#         def decorator(*args, **kwargs):
#             """处理错误响应"""
#             try:
#                 result = view(*args, **kwargs)
#             except Exception as exception:
#                 return handle_exception(view.__name__, exception, **kwargs)
#             else:
#                 if isinstance(result, Response):
#                     return result

#                 return ok_response(result)

#         # Flask 的 endpoint, 用于 url_for(endpoint) 获取 endpoint 对应的 url rule
#         endpoint = options.pop("endpoint", decorator.__name__)
#         blueprint.add_url_rule(rule, endpoint, view_func=decorator, **options)
#         return decorator

#     return wrapper

