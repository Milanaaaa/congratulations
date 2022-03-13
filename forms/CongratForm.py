from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


# форма для добавления поздравления
class CongratForm(FlaskForm):
    holiday = SelectField('Праздник', validators=[DataRequired()], validate_choice=False)
    hd_date = DateField('Дата праздника', validators=[DataRequired()])
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField("Поздравление")
    accepter = SelectField('Получатель', validate_choice=False)
    submit = SubmitField('Отправить')
