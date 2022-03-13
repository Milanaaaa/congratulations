from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# форма для добавления роли
class RoleForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Добавить')
