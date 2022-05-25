from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Repeat New Password', validators=[DataRequired()])
    submit = SubmitField('修改密码')

class LoginForm(FlaskForm):
    username = StringField("userName", validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    role = RadioField(u'身份', choices=[('student', u'学生'), ('teacher', u'老师'), ('admin', u'管理员')],validators=[DataRequired()])
    remember = BooleanField(u'记住我')
    submit = SubmitField(u'登录')



 