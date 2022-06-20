from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from apps.models import Manager, Student, Teacher

blueprint = Blueprint("/login", __name__, url_prefix='/')


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/logins', methods=['GET', 'POST'])
def logins():
    if isinstance(current_user._get_current_object(), Manager):
        logout_user()
    if current_user.is_authenticated:
        if isinstance(current_user._get_current_object(), Student):
            return redirect(url_for('/student.student_index'))
        elif isinstance(current_user._get_current_object(), Teacher):
            return redirect(url_for('/teacher.teacher_index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = [True if remember == 'on' else False][0]
        error = None
        is_student = 1
        user = Student.query.filter_by(StudentNum=username).first()
        #  判断是否为学生
        if not user:
            #  若不是，则选取老师
            is_student = 0
            user = Teacher.query.filter_by(TeacherNum=username).first()
        if not user:
            error = '学号不存在！'
        elif not user.check_password(password):
            error = '密码错误！'

        if error is None:
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('/login.index')
            if is_student:
                return redirect(url_for('/student.student_index'))
            else:
                return redirect(url_for('/teacher.teacher_index'))
        flash(error)

    return render_template('login.html')


@blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Manager.query.filter_by(ManagerNum=username).first()
        if admin is None or not admin.check_password(str(password)):
            flash('Invalid username or password!')
            return redirect(url_for('/login.admin'))
        login_user(admin)
        #  必须验证 next 参数的值。如果不验证的话，应用将会受到重定向的攻击
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('/login.admin')
        return redirect(url_for('/admin.manager'))
    return render_template('admin.html')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/login.logins'))
