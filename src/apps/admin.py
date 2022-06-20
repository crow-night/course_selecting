from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from apps import db
from apps.models import (Course, Course_select_table, Course_Teacher, Dept,
                         Major, Manager, Student, Teacher)

blueprint = Blueprint("/admin",
                      __name__,
                      url_prefix='/',
                      template_folder='templates')


@blueprint.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('admin/manager.html')
    else:
        logout_user()
        return redirect(url_for('/login'))


# 管理员管理学生信息
@blueprint.route('/student_manage', methods=['GET', 'POST'])
@login_required
def student_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {'majors': [major.MajorName for major in Major.query.all()]}
        students = Student.query.order_by(Student.MajorNum).all()
        return render_template('admin/student_manage.html',
                               info=info,
                               students=students)


# 管理员添加学生信息
@blueprint.route('/add_student', methods=[
    'POST',
])
@login_required
def add_student():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            StudentNum = request.form['StudentNum']
            MajorName = request.form['MajorName']
            MajorNum = Major.query.filter_by(
                MajorName=MajorName).first().MajorNum
            StudentName = request.form['StudentName']
            StudentSex = request.form['StudentSex']
            StudentInyear = request.form['StudentInyear']
            if not Student.query.filter_by(StudentNum=StudentNum).first():
                student = Student(StudentNum, MajorNum, StudentName,
                                  StudentSex, StudentInyear)
                db.session.add(student)
                db.session.commit()
                flash('录入学生信息成功！')
            else:
                flash('学号%s已存在！' % (StudentNum))
        return redirect(url_for('/admin.student_manage'))


# 管理员删除学生信息
@blueprint.route('/delete_student/<StudentNum>', methods=['GET', 'POST'])
@login_required
def delete_student(StudentNum):
    if isinstance(current_user._get_current_object(), Manager):
        delete_stu = Student.query.filter_by(StudentNum=StudentNum).first()
        #  先删除选课表中信息
        course_tables = Course_select_table.query.filter_by(
            StudentNum=StudentNum).all()
        for course_table in course_tables:
            db.session.delete(course_table)
        db.session.commit()
        db.session.delete(delete_stu)
        db.session.commit()
        flash('删除学生成功！')
        return redirect(url_for('/admin.student_manage'))


# 管理员查看全部教师信息
@blueprint.route('/teacher_manage', methods=['GET', 'POST'])
@login_required
def teacher_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {'depts': [dept.DeptName for dept in Dept.query.all()]}
        teachers = Teacher.query.order_by(Teacher.DeptNum).all()
        return render_template('admin/teacher_manage.html',
                               info=info,
                               teachers=teachers)


# 管理员添加教师信息
@blueprint.route('/add_teacher', methods=[
    'POST',
])
@login_required
def add_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            TeacherNum = request.form['TeacherNum']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            TeacherName = request.form['TeacherName']
            TeacherSex = request.form['TeacherSex']
            TeacherTitle = request.form['TeacherTitle']
            TeacherInyear = request.form['TeacherInyear']
            if not Teacher.query.filter_by(TeacherNum=TeacherNum).first():
                teacher = Teacher(TeacherNum, DeptNum, TeacherName, TeacherSex,
                                  TeacherInyear, TeacherTitle)
                db.session.add(teacher)
                db.session.commit()
                flash('录入教师信息成功！')
            else:
                flash('工号%s已存在!' % (TeacherNum))
        return redirect(url_for('/admin.teacher_manage'))


# 管理员查看课程信息
@blueprint.route('/course_manage', methods=['GET', 'POST'])
@login_required
def course_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'depts': [dept.DeptName for dept in Dept.query.all()],
            'courses': [course.CourseName for course in Course.query.all()],
            'teachers':
            [teacher.TeacherName for teacher in Teacher.query.all()],
        }
        courses = Course.query.order_by(Course.CourseNum).all()
    return render_template('admin/course_manage.html',
                           info=info,
                           courses=courses)


# 管理员创建课程
@blueprint.route('/add_course', methods=[
    'POST',
])
@login_required
def add_course():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseName = request.form['CourseName']
            CourseNum = request.form['CourseNum']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            CourseCredit = request.form['CourseCredit']
            CourseTime = request.form['CourseTime']
            CourseDesc = request.form['CourseDesc']
            if not Course.query.filter_by(CourseNum=CourseNum).first():
                course = Course(CourseNum, CourseName, CourseCredit,
                                CourseTime, DeptNum, CourseDesc)
                db.session.add(course)
                db.session.commit()
                flash('创建课程成功！')
            else:
                flash('课程号"%s"重复，请修改课程号！' % (CourseNum))
        return redirect(url_for('/admin.course_manage'))


# 管理员设置老师开设课程
@blueprint.route('/add_course_teacher', methods=[
    'POST',
])
@login_required
def add_course_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseName = request.form['CourseName']
            CourseNum = Course.query.filter_by(
                CourseName=CourseName).first().CourseNum
            TeacherName = request.form['TeacherName']
            TeacherNum = Teacher.query.filter_by(
                TeacherName=TeacherName).first().TeacherNum
            CourseCapacity = request.form['CourseCapacity']
            if not Course_Teacher.query.filter_by(
                    CourseNum=CourseNum, TeacherNum=TeacherNum).first():
                course_teacher = Course_Teacher(CourseNum, TeacherNum,
                                                CourseCapacity)
                db.session.add(course_teacher)
                db.session.commit()
                flash('开设课程成功！')
            else:
                flash(f'{TeacherName}老师已开设"{CourseName}"课程，请勿重复添加！')
        return redirect(url_for('/admin.course_manage'))


# 管理员删除已开设课程
@blueprint.route('/course_delete/<CourseNum>')
@login_required
def course_delete(CourseNum):
    if isinstance(current_user._get_current_object(), Manager):
        #  先删除选课信息
        course_select_tables = Course_select_table.query.filter_by(
            CourseNum=CourseNum).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        #  再删除课程与老师的对应表
        course_teachers = Course_Teacher.query.filter_by(
            CourseNum=CourseNum).all()
        for course_teacher in course_teachers:
            db.session.delete(course_teacher)
        db.session.commit()
        flash('删除教师开设课程成功！')
        #  最后删除课程
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        db.session.delete(course)
        db.session.commit()
        flash('删除课程成功！')
    return redirect(url_for('/admin.course_manage'))


# 管理员查看学生选课情况
@blueprint.route('/course_select_manage', methods=['GET', 'POST'])
@login_required
def course_select_manage():
    if isinstance(current_user._get_current_object(), Manager):
        course_teachers = Course_Teacher.query.order_by(
            Course_Teacher.CourseNum).all()
        tables = []
        for course_teacher in course_teachers:
            course = Course.query.filter_by(
                CourseNum=course_teacher.CourseNum).first()
            teacher = Teacher.query.filter_by(
                TeacherNum=course_teacher.TeacherNum).first()
            course_select_tables = Course_select_table.query.filter_by(
                CourseNum=course.CourseNum,
                TeacherNum=teacher.TeacherNum).all()
            table = {
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'TeacherNum': teacher.TeacherNum,
                'TeacherName': teacher.TeacherName,
                'CourseCapacity': course_teacher.CourseCapacity,
                'CourseStudents': len(course_select_tables),
            }
            tables.append(table)
    return render_template('admin/course_select_manage.html', tables=tables)


# 管理员删除开设课程和已参加学生
@blueprint.route('/course_teacher_delete/<CourseNum>/<TeacherNum>')
@login_required
def course_teacher_delete(CourseNum, TeacherNum):
    if isinstance(current_user._get_current_object(), Manager):
        #  先删除选课信息
        course_select_tables = Course_select_table.query.filter_by(
            CourseNum=CourseNum, TeacherNum=TeacherNum).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        #  再删除课程与老师的对应表
        course_teacher = Course_Teacher.query.filter_by(
            CourseNum=CourseNum, TeacherNum=TeacherNum).first()
        db.session.delete(course_teacher)
        db.session.commit()
        flash('删除教师开设课程成功！')
    return redirect(url_for('/admin.course_select_manage'))


# 管理员手动退课
@blueprint.route('/drop_course_select', methods=[
    'POST',
])
@login_required
def drop_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            TeacherNum = request.form['TeacherNum']
            StudentNum = request.form['StudentNum']
            course_select_table = Course_select_table.query.filter_by(
                CourseNum=CourseNum,
                TeacherNum=TeacherNum,
                StudentNum=StudentNum).first()
            if course_select_table:
                db.session.delete(course_select_table)
                db.session.commit()
                flash('手动退课成功！')
            else:
                flash('手动退课失败！学生(%s)未选择教师(%s)的课程(%s)' %
                      (StudentNum, TeacherNum, CourseNum))
    return redirect(url_for('/admin.course_select_manage'))


# 管理员扩容和缩容课程
@blueprint.route(
    '/change_course_capacity/<CourseNum>/<TeacherNum>/<add_or_sub>',
    methods=[
        'GET',
    ])
@login_required
def change_course_capacity(CourseNum, TeacherNum, add_or_sub):
    if isinstance(current_user._get_current_object(), Manager):
        course_teacher = Course_Teacher.query.filter_by(
            CourseNum=CourseNum, TeacherNum=TeacherNum).first()
        if add_or_sub == 'add':
            course_teacher.CourseCapacity += 10
            flash('课程容量扩容10人！')
        elif add_or_sub == 'sub':
            course_teacher.CourseCapacity -= 10
            flash('课程容量缩容10人！')
        db.session.commit()
    return redirect(url_for('/admin.course_select_manage'))
