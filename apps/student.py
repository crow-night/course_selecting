from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from apps import db
from apps.models import (Course, Course_select_table, Course_Teacher, Student,
                         Teacher)

blueprint = Blueprint("/student",
                      __name__,
                      url_prefix='/',
                      template_folder='templates')


@blueprint.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('student/student.html')
    else:
        logout_user()


# 学生修改密码
@blueprint.route('/student_info/<int:change>', methods=['GET', 'POST'])
@blueprint.route('/student_info',
                 defaults={'change': 0},
                 methods=['GET', 'POST'])
@login_required
def student_info(change):
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']
        if not new_password == new_password2:
            flash('两次密码输入不一致！')
        elif not current_user.check_password(old_password):
            flash('原密码输入错误！')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('/student.student_info'))
    return render_template('student/student_info.html', change=change)


# 学生已选课程显示
@blueprint.route('/course_select_table', methods=[
    'GET',
])
@login_required
def course_select_table():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course_select_table = Course_select_table.query.filter_by(
                StudentNum=current_user.StudentNum,
                CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(
                TeacherNum=course_select_table.TeacherNum).first()
            table = {
                'CourseNum': Course_.CourseNum,
                'CourseName': Course_.CourseName,
                'CourseCredit': Course_.CourseCredit,
                'CourseTime': Course_.CourseTime,
                'CourseDept': teacher.dept.DeptName,
                'TeacherName': teacher.TeacherName,
            }
            tables.append(table)
        return render_template('student/course_select_table.html',
                               tables=tables)


# 学生选课
@blueprint.route('/course_teachers/<CourseNum>', methods=[
    'GET',
])
@login_required
def course_teachers(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        course_teachers = Course_Teacher.query.filter_by(
            CourseNum=CourseNum).all()
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        tables = []
        for course_teacher in course_teachers:
            course_select_table = Course_select_table.query.filter_by(
                CourseNum=CourseNum,
                TeacherNum=course_teacher.TeacherNum).all()
            teacher = Teacher.query.filter_by(
                TeacherNum=course_teacher.TeacherNum).first()
            table = {
                'CourseNum': course_teacher.CourseNum,
                'TeacherNum': course_teacher.TeacherNum,
                'CourseName': course.CourseName,
                'TeacherName': teacher.TeacherName,
                'Time': 'TODO',
                'CourseCapacity': course_teacher.CourseCapacity,
                'CourseStudents': len(course_select_table),
            }
            tables.append(table)
        return render_template('student/course_teachers.html', tables=tables)


# 学生可选课显示
@blueprint.route('/course', methods=[
    'GET',
])
@login_required
def course():
    if isinstance(current_user._get_current_object(), Student):
        all_courses = Course.query.all()
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        tables = []
        for course in all_courses:
            table = {
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'CourseCredit': course.CourseCredit,
                'CourseTime': course.CourseTime,
                'CourseDept': course.dept.DeptName
            }
            tables.append(table)
        return render_template('student/course.html',
                               tables=tables,
                               course_selected=course_selected)


# 学生退选课程
@blueprint.route('/course_drop/<CourseNum>', methods=[
    'GET',
])
@login_required
def course_drop(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if int(CourseNum) not in course_selected:
            flash('您未选择该门课程！')
        else:
            current_user.drop_course(CourseNum)
            db.session.commit()
            flash('您已成功退选该门课程。')
        return redirect(url_for('/student.course_select_table'))


# 学生选课
@blueprint.route('/course_select/<CourseNum>/<TeacherNum>', methods=[
    'GET',
])
@login_required
def course_select(CourseNum, TeacherNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if CourseNum in course_selected:
            flash('错误：您已选课程中存在该门课程！')
        else:
            course_select = Course_select_table(current_user.StudentNum,
                                                CourseNum, TeacherNum)
            db.session.add(course_select)
            db.session.commit()
            flash('您已成功选择该门课程。')
        return redirect(url_for('/student.course'))


# 学生更换选课老师
@blueprint.route('/course_change/<CourseNum>', methods=[
    'GET',
])
@login_required
def course_change(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        current_user.drop_course(CourseNum)
        db.session.commit()
        return redirect(
            url_for('/student.course_teachers', CourseNum=CourseNum))


# 学生查询成绩
@blueprint.route('/grade_query', methods=[
    'GET',
])
@login_required
def grade_query():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course = Course.query.filter_by(
                CourseNum=Course_.CourseNum).first()
            course_select_table = Course_select_table.query.filter_by(
                StudentNum=current_user.StudentNum,
                CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(
                TeacherNum=course_select_table.TeacherNum).first()
            table = {
                'CourseNum': Course_.CourseNum,
                'CourseName': course.CourseName,
                'CourseCredit': course.CourseCredit,
                'CourseTime': course.CourseTime,
                'CourseDept': teacher.dept.DeptName,
                'TeacherName': teacher.TeacherName,
                'Grade': course_select_table.Grade,
            }
            tables.append(table)
        return render_template('student/grade_query.html', tables=tables)


# 学生专业信息
@blueprint.route('/major_info', methods=[
    'GET',
])
@login_required
def major_info():
    return render_template('student/major_info.html')


# 学生学院信息
@blueprint.route('/dept_info', methods=[
    'GET',
])
@login_required
def dept_info():
    return render_template('student/dept_info.html')
