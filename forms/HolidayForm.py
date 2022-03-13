from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


# форма для добавления праздника
class HolidayForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    hd_date = DateField('Дата праздника', validators=[DataRequired()])
    submit = SubmitField('Добавить')
