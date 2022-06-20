from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from apps import db
from apps.models import Course, Course_select_table, Student, Teacher

blueprint = Blueprint("/teacher",
                      __name__,
                      url_prefix='/',
                      template_folder='templates')


@blueprint.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('teacher/teacher.html')
    else:
        logout_user()


# 老师修改密码
@blueprint.route('/teacher_info', methods=['GET', 'POST'])
@login_required
def teacher_info():
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
        return redirect(url_for('/teacher.teacher_info'))
    return render_template('teacher/teacher_info.html')


# 老师查看学生选课信息
@blueprint.route('/course_select_detail')
@login_required
def course_select_detail():
    if isinstance(current_user._get_current_object(), Teacher):
        courses = current_user.Courses
        course_tables = []
        for course in courses:
            course_select_tables = Course_select_table.query.filter_by(
                CourseNum=course.CourseNum,
                TeacherNum=current_user.TeacherNum).all()
            course_info = {
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'CourseStudents': len(course_select_tables),
            }
            tables = []
            for course_select_table in course_select_tables:
                student = Student.query.filter_by(
                    StudentNum=course_select_table.StudentNum).first()
                table = {
                    'StudentNum': student.StudentNum,
                    'StudentName': student.StudentName,
                    'StudentSex': student.StudentSex,
                    'DeptName': student.major.dept.DeptName,
                    'MajorName': student.major.MajorName,
                }
                tables.append(table)
            course_tables.append([course_info, tables])
        return render_template('teacher/course_select_detail.html',
                               course_tables=course_tables)


# 老师查看录入的学生成绩
@blueprint.route('/course_grade_input/<CourseNum>', methods=['GET', 'POST'])
@blueprint.route('/course_grade_input', defaults={'CourseNum': 0})
@login_required
def course_grade_input(CourseNum):
    if isinstance(current_user._get_current_object(), Teacher):
        if request.method == 'POST':
            course = Course.query.filter_by(CourseNum=CourseNum).first()
            course_select_tables = Course_select_table.query.filter_by(
                CourseNum=course.CourseNum,
                TeacherNum=current_user.TeacherNum).all()
            for course_select_table in course_select_tables:
                student = Student.query.filter_by(
                    StudentNum=course_select_table.StudentNum).first()
                if not course_select_table.Grade:
                    grade = request.form[student.StudentNum]
                    course_select_table.input_grade(grade)
            db.session.commit()
            flash('成绩录入成功！')
            return redirect(url_for('/teacher.course_grade_input'))
        else:
            courses = current_user.Courses
            course_tables = []
            for course in courses:
                flag = 0
                course_select_tables = Course_select_table.query.filter_by(
                    CourseNum=course.CourseNum,
                    TeacherNum=current_user.TeacherNum).all()
                course_info = {
                    'CourseNum': course.CourseNum,
                    'CourseName': course.CourseName,
                    'CourseStudents': len(course_select_tables),
                }
                tables = []
                for course_select_table in course_select_tables:
                    student = Student.query.filter_by(
                        StudentNum=course_select_table.StudentNum).first()
                    table = {
                        'StudentNum': student.StudentNum,
                        'StudentName': student.StudentName,
                        'StudentSex': student.StudentSex,
                        'DeptName': student.major.dept.DeptName,
                        'MajorName': student.major.MajorName,
                        'Grade': course_select_table.Grade
                    }
                    if not table['Grade']:
                        flag = 1
                    tables.append(table)
                course_tables.append([course_info, tables, flag])
        return render_template('teacher/course_grade_input.html',
                               course_tables=course_tables)


# 老师修改学生成绩
@blueprint.route('/grade_set_zero/<CourseNum>/<StudentNum>')
def grade_set_zero(CourseNum, StudentNum):
    if isinstance(current_user._get_current_object(), Teacher):
        course_select_table = Course_select_table.query.filter_by(
            StudentNum=StudentNum, CourseNum=CourseNum).first()
        course_select_table.input_grade(None)
        db.session.commit()
        return redirect(url_for('/teacher.course_grade_input'))
