from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


# форма для регистрации
class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    birth_date = DateField('Дата рождения', validators=[DataRequired()])
    submit = SubmitField('Войти')
